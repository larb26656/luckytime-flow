import { sum } from './math.mjs';

const job = process.env.JOB;
if (job) {
  const { run } = await import(`./jobs/${job}.mjs`);
  await run();
} else {
  console.log(sum(2, 3));
}
