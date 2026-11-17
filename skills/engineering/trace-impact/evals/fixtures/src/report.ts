export async function revenue() {
  return db.query("SELECT SUM(amount) FROM orders WHERE status = 'PAID'");
}
// Unrelated symbol: this status belongs to a worker, not Order.
export interface Worker { status: 'IDLE' | 'RUNNING' }
