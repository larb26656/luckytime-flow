import { statusLabel } from './ui';
const jobs = {
  exportOrders: async () => (await loadOrders()).map(order => statusLabel(order.status))
};
export async function runJob(name: string) { return jobs[name](); }
// Actual job selection happens in deployment config not included here.
