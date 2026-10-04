"""Price the asks from their quantities and the rates.

src/asks.json carries no rupee amount that can be derived: each line of an ask's
price breakdown names a quantity and the rate it is paid at, and this module
does the arithmetic. The published asks.json (what ask.html reads) gets the
rendered lines, each ask's cost, and the rates strip, in the shape the page
already expects.

A basis line is one of
    {"say": "...", "qty": 300, "rate": "vidvan_hour"}   quantity x rate
    {"say": "...", "rupees": 45000}                      a fixed amount
    {"say": "..."}                                       a note, no amount
"say" may contain {qty} and {rate}; ": <amount>" is appended, then "suffix".
"""
import json
import math

LAKH = 100_000


def money(rupees):
    """₹1.5 lakh, ₹0.39 lakh, ₹1,470."""
    if rupees >= 10_000:
        v = round(rupees / LAKH, 2)
        return f'₹{v:g} lakh' if v < 100 else f'₹{v / 100:g} crore'
    return f'₹{rupees:,.0f}'


def rate_text(rate):
    r = rate['rupees']
    amount = f'₹{r / LAKH:g} lakh' if r >= LAKH else f'₹{r:,}'
    return f"{amount} {rate['per']}"


def qty_text(q):
    return f'{q:,}' if isinstance(q, int) or float(q).is_integer() else f'{q:g}'


def round_cost(lakh):
    """The figure shown on an ask: to the half lakh, or to the lakh above ₹1 crore."""
    step = 1 if lakh >= 100 else 0.5
    return round(math.floor(lakh / step + 0.5) * step, 2)


def price(src):
    rates = {r['id']: r for r in src['rates']}

    def line(b):
        if 'rate' in b:
            r = rates[b['rate']]
            amount = b['qty'] * r['rupees']
        else:
            amount = b.get('rupees')
        text = b['say'].format(qty=qty_text(b.get('qty', 0)), rate=rate_text(rates[b['rate']]) if 'rate' in b else '')
        if amount is not None:
            text += ': ' + money(amount)
        return text + b.get('suffix', ''), amount or 0

    def priced(item):
        out = {k: v for k, v in item.items() if k != 'basis'}
        lines = [line(b) for b in item['basis']]
        out['basis'] = [t for t, _ in lines]
        exact = sum(a for _, a in lines) / LAKH
        out['cost_lakh'] = round_cost(exact)
        out['_exact_lakh'] = round(exact, 4)
        return out

    pub = {k: v for k, v in src.items() if k not in ('rates', 'asks', 'program')}
    pub['rates'] = [{'label': r['label'], 'value': r.get('show', rate_text(r))} for r in src['rates'] if r.get('strip')]
    pub['asks'] = [priced(a) for a in src['asks']]
    pub['program'] = priced(src['program'])
    for a in pub['asks']:
        m = a.get('meter', {})
        if '{per_10k_verses}' in m.get('note', ''):
            m['note'] = m['note'].replace('{per_10k_verses}', money(a['cost_lakh'] * LAKH / m['target'] * 10_000))
    return pub


def published(src_path):
    """The asks.json the page reads, without the build-only fields."""
    pub = price(json.load(open(src_path, encoding='utf8')))
    for item in pub['asks'] + [pub['program']]:
        item.pop('_exact_lakh')
    return pub
