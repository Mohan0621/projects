const API_KEY = 'tiZWtwFTz8TMxoMY4aF6UMeiGh2xa0d5'; 
const BASE_URL = 'https://api.apilayer.com/fixer';

const fromCurrency = document.getElementById("from-currency");
const toCurrency = document.getElementById("to-currency");
const convertBtn = document.getElementById("convert-btn");
const resultDiv = document.getElementById("result");
const amountInput = document.getElementById("amount");

async function loadCurrencies() {
  const res = await fetch(`${BASE_URL}/symbols`, {
    headers: { apikey: API_KEY }
  });
  const data = await res.json();

  if (data.success) {
    const symbols = data.symbols;
    for (let currency in symbols) {
      const option1 = document.createElement("option");
      option1.value = currency;
      option1.text = currency;
      fromCurrency.appendChild(option1);

      const option2 = document.createElement("option");
      option2.value = currency;
      option2.text = currency;
      toCurrency.appendChild(option2);
    }

    fromCurrency.value = "USD";
    toCurrency.value = "INR";
  } else {
    alert("Failed to load currency symbols.");
  }
}

async function convertCurrency() {
  const amount = parseFloat(amountInput.value);
  const from = fromCurrency.value;
  const to = toCurrency.value;

  if (isNaN(amount) || amount <= 0) {
    resultDiv.textContent = "Enter a valid amount";
    return;
  }

  const url = `${BASE_URL}/convert?to=${to}&from=${from}&amount=${amount}`;

  try {
    const res = await fetch(url, {
      headers: { apikey: API_KEY }
    });
    const data = await res.json();

    if (data.success) {
      resultDiv.textContent = `${amount} ${from} = ${data.result.toFixed(2)} ${to}`;
    } else {
      resultDiv.textContent = "Conversion failed.";
    }
  } catch (error) {
    console.error(error);
    resultDiv.textContent = "Error fetching data.";
  }
}

convertBtn.addEventListener("click", convertCurrency);
window.addEventListener("DOMContentLoaded", loadCurrencies);
