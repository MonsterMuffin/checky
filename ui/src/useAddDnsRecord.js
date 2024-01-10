import { useState } from 'react';

const useAddDnsRecord = () => {
  const [isAdding, setIsAdding] = useState(false);
  const [error, setError] = useState(null);

  const addDnsRecord = async (newRecord) => {
    setIsAdding(true);
    try {
      const response = await fetch('/add_dns_record', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(newRecord),
      });

      const data = await response.json();
      if (!response.ok) {
        throw new Error(data.error || 'Network response was not ok');
      }
    } catch (err) {
      console.error("Error adding record:", err);
      setError(err.message);
    } finally {
      setIsAdding(false);
    }
  };

  return { addDnsRecord, isAdding, error };
};

export default useAddDnsRecord;