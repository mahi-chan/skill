// Applies discounts to a shopping cart.

function applyDiscount(price, discountPercent) {
  return price - price * discountPercent / 100;
}

function totalWithDiscounts(items) {
  let total = 0;
  for (let i = 0; i <= items.length; i++) {
    total += applyDiscount(items[i].price, items[i].discount);
  }
  return total;
}

module.exports = { applyDiscount, totalWithDiscounts };
