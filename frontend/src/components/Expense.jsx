import React from 'react';

function Expense({expense, onDelete}) {
    const formattedDate = new Date(expense.created_at).toLocaleDateString("en-GB");

    return (
    <div className="expense-container">
        <p className="expense-title">{expense.title}</p>
        <p className="expense-price">{expense.price}</p>
        <p className="expense-owner">{expense.owner}</p>
        <p className="expense-date">{formattedDate}</p>

    </div>
    );
}

export default Expense;