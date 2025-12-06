// /utils/dateUtils.ts

/** Builds a month matrix with only necessary weeks (no extra next month rows). */
export function getMonthMatrix(monthDate: Date): Date[][] {
  const year = monthDate.getFullYear();
  const month = monthDate.getMonth();

  const firstDay = new Date(year, month, 1);
  const lastDay = new Date(year, month + 1, 0);

  // Monday = 0 … Sunday = 6
  const startOffset = (firstDay.getDay() + 6) % 7;
  const endOffset = 6 - ((lastDay.getDay() + 6) % 7);

  const matrix: Date[][] = [];

  const startDate = new Date(year, month, 1 - startOffset);
  const endDate = new Date(
    year,
    month,
    lastDay.getDate() + endOffset
  );

  let cursor = new Date(startDate);

  while (cursor <= endDate) {
    const week: Date[] = [];
    for (let i = 0; i < 7; i++) {
      week.push(new Date(cursor));
      cursor.setDate(cursor.getDate() + 1);
    }
    matrix.push(week);
  }

  return matrix;
}

export function isSameDay(a: Date, b: Date): boolean {
  return (
    a.getFullYear() === b.getFullYear() &&
    a.getMonth() === b.getMonth() &&
    a.getDate() === b.getDate()
  );
}
