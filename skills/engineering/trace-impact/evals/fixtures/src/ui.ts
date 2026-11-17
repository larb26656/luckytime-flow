import type { Status } from './order';
export function statusLabel(status: Status): string {
  switch (status) {
    case 'PENDING': return 'Awaiting payment';
    case 'PAID': return 'Paid';
    default: throw new Error('Unsupported status');
  }
}
export async function orderPage(id: string) {
  const order = await fetch(`/v1/orders/${id}`).then(r => r.json());
  return statusLabel(order.status);
}
