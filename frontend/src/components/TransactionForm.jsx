import { useState } from "react";
import {
  CreditCard,
  Building,
  UserCheck,
  Search,
  AlertCircle,
  Hash,
  DollarSign,
  ArrowRightLeft,
} from "lucide-react";

const initialForm = {
  step: 1,
  type: "TRANSFER",
  amount: 181,
  oldbalanceOrg: 181,
  newbalanceOrig: 0,
  oldbalanceDest: 0,
  newbalanceDest: 0,
  isFlaggedFraud: 0,
};

function TransactionForm({ onSubmit, loading }) {
  const [form, setForm] = useState(initialForm);
  const [validationError, setValidationError] = useState("");

  function handleChange(event) {
    const { name, value } = event.target;

    setForm((previous) => ({
      ...previous,
      [name]: name === "type" ? value : Number(value),
    }));
  }

  function handleSubmit(event) {
    event.preventDefault();

    setValidationError("");

    if (form.step < 0) {
      setValidationError("Transaction step cannot be negative.");
      return;
    }

    if (form.amount < 0) {
      setValidationError("Transaction amount cannot be negative.");
      return;
    }

    if (
      form.oldbalanceOrg < 0 ||
      form.newbalanceOrig < 0 ||
      form.oldbalanceDest < 0 ||
      form.newbalanceDest < 0
    ) {
      setValidationError("Account balances cannot be negative.");
      return;
    }

    const originBalanceError =
      form.oldbalanceOrg - form.amount - form.newbalanceOrig;

    const destinationBalanceError =
      form.oldbalanceDest + form.amount - form.newbalanceDest;

    const originBalanceChange = form.oldbalanceOrg - form.newbalanceOrig;

    const destinationBalanceChange = form.newbalanceDest - form.oldbalanceDest;

    const transaction = {
      ...form,
      origin_balance_error: originBalanceError,
      destination_balance_error: destinationBalanceError,
      origin_balance_change: originBalanceChange,
      destination_balance_change: destinationBalanceChange,
    };

    onSubmit(transaction);
  }

  return (
    <form className="transaction-form" onSubmit={handleSubmit}>
      {/* Group 1: Transaction Information */}
      <div className="form-section-title">
        <CreditCard size={16} />
        <span>Transaction Information</span>
      </div>

      <div className="form-group-grid">
        <div className="form-group">
          <label htmlFor="type">Transaction Type</label>
          <select
            id="type"
            name="type"
            value={form.type}
            onChange={handleChange}
          >
            <option value="CASH_IN">CASH_IN</option>
            <option value="CASH_OUT">CASH_OUT</option>
            <option value="DEBIT">DEBIT</option>
            <option value="PAYMENT">PAYMENT</option>
            <option value="TRANSFER">TRANSFER</option>
          </select>
        </div>

        <div className="form-group">
          <label htmlFor="step">Transaction Step</label>
          <div className="input-wrapper">
            <Hash className="input-icon" size={16} />
            <input
              id="step"
              name="step"
              type="number"
              min="0"
              className="has-icon"
              value={form.step}
              onChange={handleChange}
              required
            />
          </div>
        </div>

        <div className="form-group">
          <label htmlFor="amount">Transaction Amount</label>
          <div className="input-wrapper">
            <DollarSign className="input-icon" size={16} />
            <input
              id="amount"
              name="amount"
              type="number"
              min="0"
              step="0.01"
              className="has-icon"
              value={form.amount}
              onChange={handleChange}
              required
            />
          </div>
        </div>
      </div>

      {/* Group 2: Origin Account */}
      <div className="form-section-title">
        <ArrowRightLeft size={16} />
        <span>Origin Account Details</span>
      </div>

      <div className="form-group-grid">
        <div className="form-group">
          <label htmlFor="oldbalanceOrg">Previous Origin Balance</label>
          <div className="input-wrapper">
            <DollarSign className="input-icon" size={16} />
            <input
              id="oldbalanceOrg"
              name="oldbalanceOrg"
              type="number"
              min="0"
              step="0.01"
              className="has-icon"
              value={form.oldbalanceOrg}
              onChange={handleChange}
              required
            />
          </div>
        </div>

        <div className="form-group">
          <label htmlFor="newbalanceOrig">New Origin Balance</label>
          <div className="input-wrapper">
            <DollarSign className="input-icon" size={16} />
            <input
              id="newbalanceOrig"
              name="newbalanceOrig"
              type="number"
              min="0"
              step="0.01"
              className="has-icon"
              value={form.newbalanceOrig}
              onChange={handleChange}
              required
            />
          </div>
        </div>
      </div>

      {/* Group 3: Destination Account */}
      <div className="form-section-title">
        <Building size={16} />
        <span>Destination Account Details</span>
      </div>

      <div className="form-group-grid">
        <div className="form-group">
          <label htmlFor="oldbalanceDest">Previous Destination Balance</label>
          <div className="input-wrapper">
            <DollarSign className="input-icon" size={16} />
            <input
              id="oldbalanceDest"
              name="oldbalanceDest"
              type="number"
              min="0"
              step="0.01"
              className="has-icon"
              value={form.oldbalanceDest}
              onChange={handleChange}
              required
            />
          </div>
        </div>

        <div className="form-group">
          <label htmlFor="newbalanceDest">New Destination Balance</label>
          <div className="input-wrapper">
            <DollarSign className="input-icon" size={16} />
            <input
              id="newbalanceDest"
              name="newbalanceDest"
              type="number"
              min="0"
              step="0.01"
              className="has-icon"
              value={form.newbalanceDest}
              onChange={handleChange}
              required
            />
          </div>
        </div>
      </div>

      {/* Group 4: Flagged Indicator */}
      <div className="form-section-title">
        <UserCheck size={16} />
        <span>Fraud Flags</span>
      </div>

      <div className="form-group-grid" style={{ marginBottom: "1.5rem" }}>
        <div className="form-group">
          <label htmlFor="isFlaggedFraud">Flagged Fraud Indicator</label>
          <select
            id="isFlaggedFraud"
            name="isFlaggedFraud"
            value={form.isFlaggedFraud}
            onChange={handleChange}
          >
            <option value={0}>No (0)</option>
            <option value={1}>Yes (1)</option>
          </select>
        </div>
      </div>

      {validationError && (
        <div className="validation-error" style={{ marginBottom: "1.25rem" }}>
          <AlertCircle size={18} />
          <span>{validationError}</span>
        </div>
      )}

      <button type="submit" className="analyze-button" disabled={loading}>
        {loading ? (
          <>Analyzing Transaction...</>
        ) : (
          <>
            <Search size={18} /> Analyze Transaction
          </>
        )}
      </button>
    </form>
  );
}

export default TransactionForm;