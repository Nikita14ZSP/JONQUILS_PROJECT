import React, { useState, useEffect } from "react";
import axios from "../api/api";
import { useNavigate } from "react-router-dom";

const DriverUpdatePage = () => {
  const [driverData, setDriverData] = useState({
    firstname: "",
    lastname: "",
    email: "",
    age: 0,
    driver_rating: 0,
    driver_rides: 0,
    driver_time_accidents: 0,
  });

  const [responseMessage, setResponseMessage] = useState("");
  const navigate = useNavigate();

  useEffect(() => {
    // Ideally, fetch driver data from the server or use the current logged-in user's data
    // This could be fetched via an API call
    // For example:
    // axios.get('/drivers/profile')
    //   .then(response => setDriverData(response.data))
    //   .catch(error => console.log(error));

    // For now, you can assume the data is available as an object
  }, []);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setDriverData({ ...driverData, [name]: value });
  };

  const handleUpdate = async (e) => {
    e.preventDefault();
    try {
      const endpoint = "/drivers/update";
      const payload = {
        user_data: {
          firstname: driverData.firstname,
          lastname: driverData.lastname,
          email: driverData.email,
        },
        driver_data: {
          age: driverData.age,
          driver_rating: driverData.driver_rating,
          driver_rides: driverData.driver_rides,
          driver_time_accidents: driverData.driver_time_accidents,
        },
      };

      const response = await axios.put(endpoint, payload);
      setResponseMessage("Driver information updated successfully.");
      navigate("/dashboard"); // Redirect back to the dashboard after success
    } catch (error) {
      setResponseMessage(`Error: ${error.response?.data?.detail || error.message}`);
    }
  };

  return (
    <div className="container" style={{ maxWidth: '600px', margin: '0 auto', padding: '20px', backgroundColor: '#f9f9f9', borderRadius: '10px', boxShadow: '0 4px 10px rgba(0, 0, 0, 0.1)' }}>
      <h2 style={{ textAlign: 'center', color: '#333', marginBottom: '20px', fontSize: '26px' }}>Update Driver Information</h2>
      <form onSubmit={handleUpdate} style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
        <div className="form-group" style={{ display: 'flex', flexDirection: 'column' }}>
          <label style={{ fontSize: '16px', color: '#555', marginBottom: '8px' }}>First Name:</label>
          <input
            type="text"
            name="firstname"
            value={driverData.firstname}
            onChange={handleChange}
            required
            style={{ padding: '12px', fontSize: '16px', border: '1px solid #ccc', borderRadius: '8px', outline: 'none', transition: 'border-color 0.3s ease' }}
          />
        </div>
        <div className="form-group" style={{ display: 'flex', flexDirection: 'column' }}>
          <label style={{ fontSize: '16px', color: '#555', marginBottom: '8px' }}>Last Name:</label>
          <input
            type="text"
            name="lastname"
            value={driverData.lastname}
            onChange={handleChange}
            required
            style={{ padding: '12px', fontSize: '16px', border: '1px solid #ccc', borderRadius: '8px', outline: 'none', transition: 'border-color 0.3s ease' }}
          />
        </div>
        <div className="form-group" style={{ display: 'flex', flexDirection: 'column' }}>
          <label style={{ fontSize: '16px', color: '#555', marginBottom: '8px' }}>Email:</label>
          <input
            type="email"
            name="email"
            value={driverData.email}
            onChange={handleChange}
            required
            style={{ padding: '12px', fontSize: '16px', border: '1px solid #ccc', borderRadius: '8px', outline: 'none', transition: 'border-color 0.3s ease' }}
          />
        </div>
        <div className="form-group" style={{ display: 'flex', flexDirection: 'column' }}>
          <label style={{ fontSize: '16px', color: '#555', marginBottom: '8px' }}>Age:</label>
          <input
            type="number"
            name="age"
            value={driverData.age}
            onChange={handleChange}
            required
            style={{ padding: '12px', fontSize: '16px', border: '1px solid #ccc', borderRadius: '8px', outline: 'none', transition: 'border-color 0.3s ease' }}
          />
        </div>
        <div className="form-group" style={{ display: 'flex', flexDirection: 'column' }}>
          <label style={{ fontSize: '16px', color: '#555', marginBottom: '8px' }}>Driver Rating:</label>
          <input
            type="number"
            name="driver_rating"
            value={driverData.driver_rating}
            onChange={handleChange}
            required
            style={{ padding: '12px', fontSize: '16px', border: '1px solid #ccc', borderRadius: '8px', outline: 'none', transition: 'border-color 0.3s ease' }}
          />
        </div>
        <div className="form-group" style={{ display: 'flex', flexDirection: 'column' }}>
          <label style={{ fontSize: '16px', color: '#555', marginBottom: '8px' }}>Driver Rides:</label>
          <input
            type="number"
            name="driver_rides"
            value={driverData.driver_rides}
            onChange={handleChange}
            required
            style={{ padding: '12px', fontSize: '16px', border: '1px solid #ccc', borderRadius: '8px', outline: 'none', transition: 'border-color 0.3s ease' }}
          />
        </div>
        <div className="form-group" style={{ display: 'flex', flexDirection: 'column' }}>
          <label style={{ fontSize: '16px', color: '#555', marginBottom: '8px' }}>Driver Time Accidents:</label>
          <input
            type="number"
            name="driver_time_accidents"
            value={driverData.driver_time_accidents}
            onChange={handleChange}
            required
            style={{ padding: '12px', fontSize: '16px', border: '1px solid #ccc', borderRadius: '8px', outline: 'none', transition: 'border-color 0.3s ease' }}
          />
        </div>

        <button type="submit" style={{ padding: '12px 20px', backgroundColor: '#3498db', color: 'white', fontSize: '18px', border: 'none', borderRadius: '8px', cursor: 'pointer', transition: 'background-color 0.3s ease' }}>
          Update Information
        </button>
      </form>

      {responseMessage && <p style={{ textAlign: 'center', fontSize: '16px', color: '#27ae60', marginTop: '20px' }}>{responseMessage}</p>}
    </div>
  );
};

export default DriverUpdatePage;
