import pytest
from django.urls import reverse
from django.test import RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware

from POS_app.models import Employees, MenuItems, Orders, OrderItems, ServingRules
from POS_app.views import role_required
from POS_app.business.Actors.User import Role
from POS_app.business.Services.MenuService import MenuService
from POS_app.business.Services.OrderService import OrderService
from POS_app.business.Items import Utils


def _add_session(request):
    """Dodaje request.session do RequestFactory request."""
    middleware = SessionMiddleware(lambda r: None)
    middleware.process_request(request)
    request.session.save()
    return request


@pytest.fixture
def waiter(db):
    # Hasło musi przejść password_validator: min 8, znak specjalny z listy, cyfra
    return Employees.objects.create(
        _name="Waiter One",
        _login="waiter@example.com",
        _password="Secret_1!",
        _role=Role.WAITER.name,
    )


@pytest.fixture
def manager(db):
    return Employees.objects.create(
        _name="Manager One",
        _login="manager@example.com",
        _password="Secret_1!",
        _role=Role.MANAGER.name,
    )


@pytest.fixture
def menu_items(db):
    m1 = MenuItems.objects.create(
        name="Pizza",
        price=30.00,
        prep_time_min=10,
        active=True,
        course="Main",
        tax=8.00,
    )
    m2 = MenuItems.objects.create(
        name="Cola",
        price=8.00,
        prep_time_min=1,
        active=True,
        course="Drink",
        tax=8.00,
    )
    return [m1, m2]


@pytest.mark.django_db
def test_login_success_sets_session(client, waiter):
    """
    Test #1: poprawne logowanie -> session ustawiona + redirect do panelu roli.
    Nasz login_view czyta POST: login/password, a URL name to login_site.
    """
    url = reverse("login_site")
    resp = client.post(url, {"login": waiter._login, "password": "Secret_1!"})

    assert resp.status_code == 302  # redirect
    session = client.session
    assert session["user_login"] == waiter._login
    assert session["user_name"] == waiter._name
    assert session["user_role"] == Role.WAITER.name


@pytest.mark.django_db
def test_login_wrong_password_does_not_set_session(client, waiter):
    """
    Test #2: złe hasło -> render login.html z błędem, bez session user_*.
    """
    url = reverse("login_site")
    resp = client.post(url, {"login": waiter._login, "password": "BadPass_1!"})

    assert resp.status_code == 200  # render strony
    session = client.session
    assert session.get("user_login") is None
    assert session.get("user_role") is None


@pytest.mark.django_db
def test_role_required_redirects_when_wrong_role():
    """
    Test #3: role_required ma redirectować do login_site, gdy rola nie pasuje.
    """
    rf = RequestFactory()

    @role_required([Role.MANAGER.name])
    def dummy_view(request):
        return "OK"

    req = _add_session(rf.get("/manager/"))
    req.session["user_role"] = Role.WAITER.name

    resp = dummy_view(req)
    assert resp.status_code == 302
    # docelowo redirect do login_site
    assert resp.url.endswith(reverse("login_site"))


@pytest.mark.django_db
def test_menu_service_add_creates_item(manager):
    """
    Test #4: MenuService._add zapisuje MenuItems (przez full_clean + save).
    """
    service = MenuService()
    result = service._add(("Burger", 25.0, 12, "on", "Main", 8.0))

    assert "success" in result
    assert MenuItems.objects.filter(name="Burger").exists()
    item = MenuItems.objects.get(name="Burger")
    assert float(item.price) == 25.0
    assert item.active is True


@pytest.mark.django_db
def test_order_service_create_creates_order_items_and_serving_rules(waiter, menu_items):
    """
    Test #5: OrderService.create tworzy Orders + OrderItems + ServingRules.
    """
    service = OrderService()
    payload_items = [
        {"menu_item_id": menu_items[0].m_id, "quantity": 2},
        {"menu_item_id": menu_items[1].m_id, "quantity": 1},
    ]

    result = service.create(
        waiter_login=waiter._login,
        is_takeaway=False,
        table_no=12,
        notes="No onions",
        items=payload_items,
    )

    assert "success" in result
    order = result["order"]
    assert Orders.objects.filter(o_id=order.o_id).exists()

    # 2 pozycje zamówienia
    assert OrderItems.objects.count() == 2
    # ServingRules łączą zamówienie z itemami
    assert ServingRules.objects.filter(o_id=order).count() == 2


@pytest.mark.django_db
def test_cancel_order_blocked_when_paid(waiter):
    """
    Test #6: cancel zablokowany dla PAID/ARCHIVED.
    """
    order = Orders.objects.create(
        waiter=waiter,
        displayed_id=1,
        status=Utils.OrderStatus.PAID.name,
        is_takeaway=False,
        table_no=1,
        notes="",
    )

    service = OrderService()
    res = service.cancel(order.o_id)

    order.refresh_from_db()
    assert order.status == Utils.OrderStatus.PAID.name
    assert "error" in res
