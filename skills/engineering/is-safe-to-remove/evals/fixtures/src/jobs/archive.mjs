globalThis.auditJobs ??= new Set();
globalThis.auditJobs.add('auditArchive');

export async function run() {
  console.log('archive job: auditArchive registered');
}
