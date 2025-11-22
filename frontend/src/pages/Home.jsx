import { useState, useEffect } from 'react';
import api from '../api';
import Expense from '../components/Expense';

function Home() {
    const [expenses, setExpenses] = useState([]);

    useEffect(() => {
        getExpenses();
    }, [])

    const getExpenses = () => {
        api
            .get("/api/expenses/")
            .then(res => res.data)
            .then((data) => {
                setExpenses(data);
                console.log(data)
            })
            .catch(err => alert(err));
    };

    const deleteExpense = (id) => {
        api.delete(`/api/expenses/${id}/`).then(res => {
            if (res.status === 204) alert("Expense deleted successfully");
            else alert("Error deleting expense");
            getExpenses();
        }).catch(err => alert(err));
    };

    return <div>
        <div>
            <h2>Expenses</h2>
            {expenses.map((expense) => <Expense expense={expense} onDelete={deleteExpense} key={expense.id}/>)}
        </div>
    </div>
}

export default Home;
