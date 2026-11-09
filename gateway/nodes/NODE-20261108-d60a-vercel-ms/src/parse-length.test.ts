import { describe, expect, it } from '@jest/globals';
import { parse } from './index';

describe('parse(string) length boundary', () => {
  it('accepts a string of exactly 100 characters', () => {
    const value = '1'.repeat(100);
    expect(value).toHaveLength(100);
    expect(Number.isFinite(parse(value))).toBe(true);
  });

  it('throws on a string of 101 characters with the corrected message', () => {
    const value = '1'.repeat(101);
    expect(value).toHaveLength(101);
    expect(() => parse(value)).toThrow(/length between 1 and 100/);
  });
});
