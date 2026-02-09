from __future__ import annotations

from datetime import date
from decimal import Decimal
from pathlib import Path

from django.conf import settings
from django.utils import timezone

from POS_app.models import Orders, ServingRules


class ReportingService:
    def __init__(self):
        print("Business logic for reporting and analytics")

    def generate_financial_report(
        self,
        date_from: date | None,
        date_to: date | None,
        requested_by: str,
    ) -> Path:
        orders_qs = Orders.objects.filter(paid_at__isnull=False).order_by("paid_at")
        if date_from:
            orders_qs = orders_qs.filter(paid_at__date__gte=date_from)
        if date_to:
            orders_qs = orders_qs.filter(paid_at__date__lte=date_to)

        orders = list(orders_qs)
        rules = ServingRules.objects.filter(o_id__in=orders).select_related(
            "o_id",
            "oi_id__m_id",
        )

        rules_by_order: dict[int, list[ServingRules]] = {}
        for rule in rules:
            rules_by_order.setdefault(rule.o_id_id, []).append(rule)

        report_lines = []
        now = timezone.now()
        period_from = date_from.isoformat() if date_from else "all"
        period_to = date_to.isoformat() if date_to else "all"

        report_lines.append("Financial Report")
        report_lines.append(f"Generated at: {now.strftime('%Y-%m-%d %H:%M:%S %Z')}")
        report_lines.append(f"Requested by: {requested_by}")
        report_lines.append(f"Period (paid_at): {period_from} to {period_to}")
        report_lines.append("")
        report_lines.append("Orders:")

        total_revenue = Decimal("0.00")

        if not orders:
            report_lines.append("No paid orders found for selected period.")
        else:
            for order in orders:
                order_total = self._calculate_order_total(rules_by_order.get(order.o_id, []))
                total_revenue += order_total
                paid_at = order.paid_at.strftime("%Y-%m-%d %H:%M:%S") if order.paid_at else "n/a"
                report_lines.append(
                    f"- Order {order.o_id} (display {order.displayed_id}) "
                    f"paid_at {paid_at} total {order_total:.2f} ZLOTY"
                )

        report_lines.append("")
        report_lines.append(f"Total orders: {len(orders)}")
        report_lines.append(f"Total revenue: {total_revenue:.2f} ZLOTY")

        reports_dir = Path(settings.BASE_DIR) / "reports"
        reports_dir.mkdir(parents=True, exist_ok=True)
        timestamp = now.strftime("%Y%m%d_%H%M%S")
        report_filename = f"financial_report_{period_from}_{period_to}_{timestamp}.txt"
        report_path = reports_dir / report_filename

        report_path.write_text("\n".join(report_lines), encoding="utf-8")
        return report_path

    def _calculate_order_total(self, rules: list[ServingRules]) -> Decimal:
        total = Decimal("0.00")
        for rule in rules:
            order_item = rule.oi_id
            menu_item = order_item.m_id
            tax = menu_item.tax / Decimal("100")
            subtotal = order_item.quantity * menu_item.price * (Decimal("1.00") + tax)
            total += subtotal
        return total
