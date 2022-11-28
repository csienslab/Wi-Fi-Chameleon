export const epoch_to_time = (epoch) => {
  const d = new Date(epoch);
  return `${d.toLocaleTimeString()} ${d.toLocaleDateString()}`;
}