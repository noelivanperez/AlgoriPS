import parseMetrics from '../metricsParser';

describe('parseMetrics', () => {
  test('parses valid metrics', () => {
    const text = '# comment\nrequests_total 5';
    expect(parseMetrics(text)).toEqual([{ name: 'requests_total', value: 5 }]);
  });

  test('throws on malformed line', () => {
    expect(() => parseMetrics('badline')).toThrow();
  });

  test('throws on invalid value', () => {
    expect(() => parseMetrics('requests_total abc')).toThrow();
  });
});
