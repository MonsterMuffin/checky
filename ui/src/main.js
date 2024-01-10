import React, { useState, useEffect } from 'react';
import {
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  CircularProgress,
  Alert,
  IconButton,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
  Button,
  Fab,
  TextField
} from '@mui/material';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import Typography from '@mui/material/Typography';
import AddIcon from '@mui/icons-material/Add';
import DeleteIcon from '@mui/icons-material/Delete';
import InfoIcon from '@mui/icons-material/Info';
import useAddDnsRecord from './useAddDnsRecord';

function DnsRecordsTable() {
  const [records, setRecords] = useState([]);
  const [loading, setLoading] = useState(false);
  const [fetchError, setFetchError] = useState(null);
  const [openAddDialog, setOpenAddDialog] = useState(false);
  const [newRecordName, setNewRecordName] = useState('');
  const [recordToDelete, setRecordToDelete] = useState(null);
  const [selectedRecord, setSelectedRecord] = useState(null);

  const { addDnsRecord, isAdding, error } = useAddDnsRecord();

  const darkTheme = createTheme({
    palette: {
      mode: 'dark',
      primary: {
        main: '#00a8d7',
      },
      background: {
        default: '#232f3e',
        paper: '#131921',
      },
    },
  });

  const sortRecordsByExpiryDate = (records) => {
    return records.sort((a, b) => {
      const dateA = new Date(a.expiry_date);
      const dateB = new Date(b.expiry_date);
      return dateA - dateB;
    });
  };

  const fetchDataAndSort = () => {
    setLoading(true);
    fetch('/metrics_json')
      .then(response => response.json())
      .then(data => {
        const sortedData = sortRecordsByExpiryDate(data);
        setRecords(sortedData);
        setLoading(false);
      })
      .catch(error => {
        console.error('Error fetching data: ', error);
        setFetchError(error);
        setLoading(false);
      });
  };

  useEffect(() => {
    fetchDataAndSort();
  }, []);

  const fetchData = () => {
    setLoading(true);
    fetch('/metrics_json')
      .then(response => response.json())
      .then(data => {
        setRecords(data);
        setLoading(false);
      })
      .catch(error => {
        console.error('Error fetching data: ', error);
        setFetchError(error);
        setLoading(false);
      });
  };

  const handleAddRecordSubmit = () => {
    const newRecord = { name: newRecordName };
    addDnsRecord(newRecord).then(() => {
      fetchDataAndSort();
      setOpenAddDialog(false);
      setNewRecordName('');
    });
  };

  const calculateTimeUntilExpiry = (expiryDate) => {
    const now = new Date();
    const expiry = new Date(expiryDate);
    const timeDiff = expiry - now;
    const daysUntilExpiry = Math.floor(timeDiff / (1000 * 60 * 60 * 24));
    return daysUntilExpiry;
  };

  const handleDeleteRecord = (recordId) => {
    fetch(`/remove_dns_record/${recordId}`, {
      method: 'DELETE',
    })
    .then(response => {
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      fetchData();
    })
    .catch(error => {
      console.error('Error deleting DNS record:', error);
    });
  };

  const handleMoreInfo = (record) => {
    setSelectedRecord(record);
  };

  if (loading) {
    return <CircularProgress />;
  }

  if (error) {
    return <Alert severity="error">An error occurred while fetching data.</Alert>;
  }

  return (
    <>
      <ThemeProvider theme={darkTheme}>
        <Fab color="primary" aria-label="add" style={{ position: 'fixed', bottom: 16, right: 16 }} onClick={() => setOpenAddDialog(true)}>
          <AddIcon />
        </Fab>
        {error && <Alert severity="error">{error}</Alert>}
        <TableContainer component={Paper}>
          <Table sx={{ minWidth: 650 }} aria-label="simple table">
            <TableHead>
              <TableRow>
                <TableCell>Name</TableCell>
                <TableCell align="right">Expiry</TableCell>
                <TableCell align="right">TLS Version</TableCell>
                <TableCell align="right">Issuer</TableCell>
                <TableCell align="right">Actions</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {records.map((record) => (
   <TableRow key={record.id}>
   <TableCell component="th" scope="row">{record.name}</TableCell>
   <TableCell align="right">
     {
       (() => {
         const daysUntilExpiry = calculateTimeUntilExpiry(record.expiry_date);
         const isExpiringSoon = daysUntilExpiry <= 14;
         return (
           <span style={{
             fontWeight: isExpiringSoon ? 'bold' : 'normal',
             color: isExpiringSoon ? 'red' : 'inherit'
           }}>
             {daysUntilExpiry > 0 ? `${daysUntilExpiry} days` : 'Expired'}
           </span>
         );
       })()
     }
   </TableCell>
   <TableCell align="right">{record.tls_version}</TableCell>
   <TableCell align="right">{record.issuer}</TableCell>
   <TableCell align="right">
     <IconButton aria-label="info" onClick={() => handleMoreInfo(record)}>
       <InfoIcon />
     </IconButton>
     <IconButton aria-label="delete" onClick={() => setRecordToDelete(record)}>
       <DeleteIcon />
     </IconButton>
   </TableCell>
 </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
        <Dialog
          open={selectedRecord !== null}
          onClose={() => setSelectedRecord(null)}
        >
          <DialogTitle>Record Details</DialogTitle>
          <DialogContent>
            <Typography>Name: {selectedRecord?.name}</Typography>
            <Typography>Expiry Date: {selectedRecord?.expiry_date}</Typography>
            <Typography>Issued Date: {selectedRecord?.issued_date}</Typography>
            <Typography>Issuer: {selectedRecord?.issuer}</Typography>
            <Typography>SANs: {selectedRecord?.sans}</Typography>
            <Typography>Serial Number: {selectedRecord?.serial_number}</Typography>
            <Typography>Signature Algorithm: {selectedRecord?.signature_algorithm || 'N/A'}</Typography>
            <Typography>Subject: {selectedRecord?.subject}</Typography>
            <Typography>TLS Version: {selectedRecord?.tls_version}</Typography>
            <Typography>Version: {selectedRecord?.version}</Typography>
          </DialogContent>
          <DialogActions>
            <Button onClick={() => setSelectedRecord(null)}>Close</Button>
          </DialogActions>
        </Dialog>
        <Dialog open={openAddDialog} onClose={() => setOpenAddDialog(false)}>
          <DialogTitle>Add New DNS Record</DialogTitle>
          <DialogContent>
            <TextField
              label="DNS Record"
              value={newRecordName}
              onChange={(e) => setNewRecordName(e.target.value)}
            />
          </DialogContent>
          <DialogActions>
            <Button onClick={() => setOpenAddDialog(false)}>Cancel</Button>
            <Button onClick={() => handleAddRecordSubmit()}>Add Record</Button>
          </DialogActions>
        </Dialog>
        <Dialog
        open={recordToDelete !== null}
        onClose={() => setRecordToDelete(null)}
      >
        <DialogTitle>Confirm Deletion</DialogTitle>
        <DialogContent>
          Are you sure you want to delete this record?
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setRecordToDelete(null)}>Cancel</Button>
          <Button onClick={() => {
            handleDeleteRecord(recordToDelete.id);
            setRecordToDelete(null);
          }}>Delete</Button>
        </DialogActions>
      </Dialog>
    </ThemeProvider>
  </>
);
}

export default DnsRecordsTable;