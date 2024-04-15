import axios from 'axios';
import { useEffect, useState } from 'react';

const Home: React.FC = () => {
    const [message, setMessage] = useState<string>('');
    const [tickets, setTickets] = useState([]);

    useEffect(() => {
        // Fetch message
        const fetchMessage = async () => {
            try {
                const response = await axios.get('http://localhost:5000/api/message');
                setMessage(response.data.message);
            } catch (error) {
                console.error('There was an error fetching the data:', error);
                setMessage('Failed to fetch data');
            }
        };

        // Fetch tickets
        const fetchTickets = () => {
            axios.get('http://localhost:5000/api/zendesk/tickets')
                .then(response => {
                    setTickets(response.data);
                })
                .catch(error => console.error('Error fetching tickets:', error));
        };

        fetchMessage();
        fetchTickets();
    }, []);

    return (
        <div className="container mx-auto px-4">
            <h1 className="text-3xl font-bold underline">Next.js Frontend</h1>
            <p className="mt-4 text-lg">{message}</p>
            <div>
                {tickets.map(ticket => (
                    <div key={ticket.id}>
                        <h3>{ticket.subject}</h3>
                        <p>{ticket.description}</p>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default Home;
