it('pays a pending order', async () => {
  const order = { id: '1', status: 'PENDING' };
  await pay(order, new MemoryOrderStore());
  expect(order.status).toBe('PAID');
});
it('shows paid label', () => {
  expect(statusLabel('PAID')).toBe('Paid');
});
it('gets order', async () => {
  const response = await request.get('/v1/orders/1');
  expect(response.status).toBe(200);
});
