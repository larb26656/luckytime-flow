export type Status = 'PENDING' | 'PAID';
export interface Order { id: string; status: Status }
export interface OrderStore { save(order: Order): Promise<void> }
export class SqlOrderStore implements OrderStore {
  async save(order: Order): Promise<void> {
    await db.execute('INSERT INTO orders (id, status) VALUES (?, ?)', [order.id, order.status]);
  }
}
export class MemoryOrderStore implements OrderStore {
  async save(order: Order): Promise<void> { memory.set(order.id, order); }
}
export async function pay(order: Order, store: OrderStore): Promise<void> {
  if (order.status !== 'PENDING') throw new Error('invalid transition');
  order.status = 'PAID';
  await store.save(order);
}
