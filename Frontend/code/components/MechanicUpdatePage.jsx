import React, { useState, useEffect } from "react";
import axios from "../api/api";
import { useNavigate } from "react-router-dom";

const MechanicUpdatePage = () => {
  const [mechanicData, setMechanicData] = useState({
    firstname: "",
    lastname: "",
    email: "",
    age: 0,
    mechanic_rating: 0,
    car_times_repaired: 0,
  });

  const [responseMessage, setResponseMessage] = useState("");
  const navigate = useNavigate();

  useEffect(() => {
    // Ideally, fetch mechanic data from the server or use the current logged-in user's data
    // This could be fetched via an API call
    // For example:
    // axios.get('/mechanics/profile')
    //   .then(response => setMechanicData(response.data))
    //   .catch(error => console.log(error));

    // For now, you can assume the data is available as an object
  }, []);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setMechanicData({ ...mechanicData, [name]: value });
  };

  const handleUpdate = async (e) => {
    e.preventDefault();
    try {
      const endpoint = "/mechanics/update";
      const payload = {
        user_data: {
          firstname: mechanicData.firstname,
          lastname: mechanicData.lastname,
          email: mechanicData.email,
        },
        mechanic_data: {
          age: mechanicData.age,
          mechanic_rating: mechanicData.mechanic_rating,
          car_times_repaired: mechanicData.car_times_repaired,
        },
      };

      const response = await axios.put(endpoint, payload);
      setResponseMessage("Mechanic information updated successfully.");
      navigate("/dashboard"); // Redirect back to the dashboard after success
    } catch (error) {
      setResponseMessage(`Error: ${error.response?.data?.detail || error.message}`);
    }
  };

  return (
    <div className="container" style={{ maxWidth: '600px', margin: '0 auto', padding: '20px', backgroundColor: '#f9f9f9', borderRadius: '10px', boxShadow: '0 4px 10px rgba(0, 0, 0, 0.1)' }}>
      <h2 style={{ textAlign: 'center', color: '#333', marginBottom: '20px', fontSize: '26px' }}>Update Mechanic Information</h2>
      <form onSubmit={handleUpdate} style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
        <div className="form-group" style={{ display: 'flex', flexDirection: 'column' }}>
          <label style={{ fontSize: '16px', color: '#555', marginBottom: '8px' }}>First Name:</label>
          <input
            type="text"
            name="firstname"
            value={mechanicData.firstname}
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
            value={mechanicData.lastname}
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
            value={mechanicData.email}
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
            value={mechanicData.age}
            onChange={handleChange}
            required
            style={{ padding: '12px', fontSize: '16px', border: '1px solid #ccc', borderRadius: '8px', outline: 'none', transition: 'border-color 0.3s ease' }}
          />
        </div>
        <div className="form-group" style={{ display: 'flex', flexDirection: 'column' }}>
          <label style={{ fontSize: '16px', color: '#555', marginBottom: '8px' }}>Mechanic Rating:</label>
          <input
            type="number"
            name="mechanic_rating"
            value={mechanicData.mechanic_rating}
            onChange={handleChange}
            required
            style={{ padding: '12px', fontSize: '16px', border: '1px solid #ccc', borderRadius: '8px', outline: 'none', transition: 'border-color 0.3s ease' }}
          />
        </div>
        <div className="form-group" style={{ display: 'flex', flexDirection: 'column' }}>
          <label style={{ fontSize: '16px', color: '#555', marginBottom: '8px' }}>Car Times Repaired:</label>
          <input
            type="number"
            name="car_times_repaired"
            value={mechanicData.car_times_repaired}
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

export default MechanicUpdatePage;
