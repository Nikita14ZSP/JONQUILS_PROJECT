import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import RegistrationForm from './components/RegistrationForm';
import MechanicUpdatePage from './components/MechanicUpdatePage';
import DriverUpdatePage from './components/DriverUpdatePage';
import AdminPageM from './components/AdminPageM';
import AdminPageDrivers from './components/AdminPageDrivers';
import AdminPageMain from './components/AdminPageMain';
import AdminPageCars from './components/AdminPageCars';
import AdminPageFixes from './components/AdminPageFixes';
import AdminPageRides from './components/AdminPageRides';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<RegistrationForm />} />
        <Route path="/mechanic-update" element={<MechanicUpdatePage />} />
        <Route path="/admin-page-mechanics" element={<AdminPageM />} />
        <Route path="/admin-page-main" element={<AdminPageMain />} />
        <Route path="/driver-update" element={<DriverUpdatePage />} />
        <Route path="/admin-page-drivers" element={<AdminPageDrivers />} />
        <Route path="/admin-page-cars" element={<AdminPageCars />} />
        <Route path="/admin-page-fixes" element={<AdminPageFixes />} />
        <Route path="/admin-page-rides" element={<AdminPageRides />} />
        {/* Перенаправление для неизвестных путей */}
        <Route path="*" element={<Navigate to="/" />} />
      </Routes>
    </Router>
  );
}

export default App;
