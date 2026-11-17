import { pay, SqlOrderStore } from './order';
router.post('/orders/:id/pay', async (req, res) => {
  await pay(await loadOrder(req.params.id), new SqlOrderStore());
  res.status(204).end();
});
// This exported endpoint is also consumed outside this repository.
router.get('/v1/orders/:id', async (req, res) => {
  const order = await loadOrder(req.params.id);
  res.json({ id: order.id, status: order.status });
});
