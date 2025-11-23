// /utils/dateUtils.ts

/**
 * Returns a 6x7 matrix of Date objects representing the calendar view.
 */
export function getMonthMatrix(monthDate: Date): Date[][] {
  const year = monthDate.getFullYear();
  const month = monthDate.getMonth();

  const firstDayOfMonth = new Date(year, month, 1);
  const startDay = (firstDayOfMonth.getDay() + 6) % 7; // Monday = 0

  const daysInMonth = new Date(year, month + 1, 0).getDate();
  const daysInPrevMonth = new Date(year, month, 0).getDate();

  const matrix: Date[][] = [];
  let currentDay = 1;
  let nextMonthDay = 1;

  for (let week = 0; week < 6; week++) {
    const row: Date[] = [];

    for (let day = 0; day < 7; day++) {
      if (week === 0 && day < startDay) {
        row.push(
          new Date(year, month - 1, daysInPrevMonth - (startDay - day - 1))
        );
      } else if (currentDay > daysInMonth) {
        row.push(new Date(year, month + 1, nextMonthDay++));
      } else {
        row.push(new Date(year, month, currentDay++));
      }
    }

    matrix.push(row);
  }

  return matrix;
}
export function isSameDay(d1: Date, d2: Date): boolean {
  return (
    d1.getFullYear() === d2.getFullYear() &&
    d1.getMonth() === d2.getMonth() &&
    d1.getDate() === d2.getDate()
  );
}

