import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Layout from './components/Layout';
import Vehicles from './pages/Vehicles';
import Sales from './pages/Sales';
import Payments from './pages/Payments';
import Home from './pages/Home';

const App: React.FC = () => {
  return (
    <Router>
      <Layout>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/vehicles" element={<Vehicles />} />
          <Route path="/sales" element={<Sales />} />
          <Route path="/payments" element={<Payments />} />
        </Routes>
      </Layout>
    </Router>
  );
};

export default App; 