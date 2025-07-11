import React, { useState, useEffect } from 'react';
import './App.css';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001';

function App() {
  const [currentView, setCurrentView] = useState('dashboard');
  const [customers, setCustomers] = useState([]);
  const [stats, setStats] = useState({});
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');

  // Fetch customers and stats
  const fetchData = async () => {
    setLoading(true);
    try {
      const [customersRes, statsRes] = await Promise.all([
        fetch(`${BACKEND_URL}/api/customers`),
        fetch(`${BACKEND_URL}/api/stats`)
      ]);

      if (customersRes.ok) {
        const customersData = await customersRes.json();
        setCustomers(customersData);
      }

      if (statsRes.ok) {
        const statsData = await statsRes.json();
        setStats(statsData);
      }
    } catch (error) {
      setMessage('Error fetching data: ' + error.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  // Customer signup form
  const CustomerSignupForm = () => {
    const [formData, setFormData] = useState({
      name: '',
      phone_number: '',
      email: '',
      date_of_birth: '',
      customer_type: 'subscription'
    });

    const handleSubmit = async (e) => {
      e.preventDefault();
      setLoading(true);
      setMessage('');

      try {
        const response = await fetch(`${BACKEND_URL}/api/customers/signup`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(formData),
        });

        if (response.ok) {
          const customer = await response.json();
          setMessage(`✅ Welcome to Birthday Club! Your account number is: ${customer.account_number}`);
          setFormData({
            name: '',
            phone_number: '',
            email: '',
            date_of_birth: '',
            customer_type: 'subscription'
          });
          fetchData(); // Refresh data
        } else {
          const error = await response.json();
          setMessage(`❌ Error: ${error.detail}`);
        }
      } catch (error) {
        setMessage(`❌ Error: ${error.message}`);
      } finally {
        setLoading(false);
      }
    };

    return (
      <div className="form-container">
        <h2>🎉 Join the Birthday Club</h2>
        <form onSubmit={handleSubmit} className="signup-form">
          <div className="form-group">
            <label>Full Name *</label>
            <input
              type="text"
              value={formData.name}
              onChange={(e) => setFormData({...formData, name: e.target.value})}
              required
            />
          </div>

          <div className="form-group">
            <label>Phone Number *</label>
            <input
              type="tel"
              value={formData.phone_number}
              onChange={(e) => setFormData({...formData, phone_number: e.target.value})}
              required
            />
          </div>

          <div className="form-group">
            <label>Email Address *</label>
            <input
              type="email"
              value={formData.email}
              onChange={(e) => setFormData({...formData, email: e.target.value})}
              required
            />
          </div>

          <div className="form-group">
            <label>Date of Birth *</label>
            <input
              type="date"
              value={formData.date_of_birth}
              onChange={(e) => setFormData({...formData, date_of_birth: e.target.value})}
              required
            />
          </div>

          <div className="form-group">
            <label>Customer Type *</label>
            <select
              value={formData.customer_type}
              onChange={(e) => setFormData({...formData, customer_type: e.target.value})}
              required
            >
              <option value="subscription">Subscription</option>
              <option value="non_subscription">Non-Subscription</option>
              <option value="corporate">Corporate</option>
            </select>
          </div>

          <button type="submit" disabled={loading} className="submit-btn">
            {loading ? 'Signing Up...' : 'Join Birthday Club'}
          </button>
        </form>
      </div>
    );
  };

  // Customer profile form
  const CustomerProfileForm = () => {
    const [accountNumber, setAccountNumber] = useState('');
    const [profileData, setProfileData] = useState({
      account_number: '',
      contact_name: '',
      email_address: '',
      employment_title: '',
      phone_number: '',
      birthday_date: '',
      favorite_bistro_food_items: '',
      preferred_bistro_beverage: '',
      interest_in_group_private_package: '',
      music_ambiance_preference: '',
      allergies: '',
      dietary_restrictions: '',
      celebration_budget: '',
      group_size_solo: '',
      preferred_contact_method: '',
      want_corporate_offers: false,
      preferred_celebration_style: '',
      personalized_bistro_birthday_treats: '',
      interest_in_rewards: false,
      i_like_surprises: false,
      special_notes: ''
    });

    const handleSubmit = async (e) => {
      e.preventDefault();
      setLoading(true);
      setMessage('');

      try {
        const response = await fetch(`${BACKEND_URL}/api/customers/${accountNumber}/profile`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(profileData),
        });

        if (response.ok) {
          const customer = await response.json();
          setMessage(`✅ Profile completed! Your profile number is: ${customer.customer_profile_number}`);
          setAccountNumber('');
          setProfileData({
            account_number: '',
            contact_name: '',
            email_address: '',
            employment_title: '',
            phone_number: '',
            birthday_date: '',
            favorite_bistro_food_items: '',
            preferred_bistro_beverage: '',
            interest_in_group_private_package: '',
            music_ambiance_preference: '',
            allergies: '',
            dietary_restrictions: '',
            celebration_budget: '',
            group_size_solo: '',
            preferred_contact_method: '',
            want_corporate_offers: false,
            preferred_celebration_style: '',
            personalized_bistro_birthday_treats: '',
            interest_in_rewards: false,
            i_like_surprises: false,
            special_notes: ''
          });
          fetchData(); // Refresh data
        } else {
          const error = await response.json();
          setMessage(`❌ Error: ${error.detail}`);
        }
      } catch (error) {
        setMessage(`❌ Error: ${error.message}`);
      } finally {
        setLoading(false);
      }
    };

    return (
      <div className="form-container">
        <h2>📝 Complete Your Profile</h2>
        <div className="account-lookup">
          <label>Account Number *</label>
          <input
            type="text"
            value={accountNumber}
            onChange={(e) => setAccountNumber(e.target.value)}
            placeholder="Enter your account number (e.g., SAN-00001)"
            required
          />
        </div>

        <form onSubmit={handleSubmit} className="profile-form">
          <div className="form-row">
            <div className="form-group">
              <label>Contact Name *</label>
              <input
                type="text"
                value={profileData.contact_name}
                onChange={(e) => setProfileData({...profileData, contact_name: e.target.value})}
                required
              />
            </div>
            <div className="form-group">
              <label>Email Address *</label>
              <input
                type="email"
                value={profileData.email_address}
                onChange={(e) => setProfileData({...profileData, email_address: e.target.value})}
                required
              />
            </div>
          </div>

          <div className="form-row">
            <div className="form-group">
              <label>Employment Title</label>
              <input
                type="text"
                value={profileData.employment_title}
                onChange={(e) => setProfileData({...profileData, employment_title: e.target.value})}
              />
            </div>
            <div className="form-group">
              <label>Phone Number *</label>
              <input
                type="tel"
                value={profileData.phone_number}
                onChange={(e) => setProfileData({...profileData, phone_number: e.target.value})}
                required
              />
            </div>
          </div>

          <div className="form-group">
            <label>Birthday Date *</label>
            <input
              type="date"
              value={profileData.birthday_date}
              onChange={(e) => setProfileData({...profileData, birthday_date: e.target.value})}
              required
            />
          </div>

          <div className="form-row">
            <div className="form-group">
              <label>Favorite Bistro Food Items</label>
              <input
                type="text"
                value={profileData.favorite_bistro_food_items}
                onChange={(e) => setProfileData({...profileData, favorite_bistro_food_items: e.target.value})}
              />
            </div>
            <div className="form-group">
              <label>Preferred Bistro Beverage</label>
              <input
                type="text"
                value={profileData.preferred_bistro_beverage}
                onChange={(e) => setProfileData({...profileData, preferred_bistro_beverage: e.target.value})}
              />
            </div>
          </div>

          <div className="form-row">
            <div className="form-group">
              <label>Interest in Group/Private Package</label>
              <select
                value={profileData.interest_in_group_private_package}
                onChange={(e) => setProfileData({...profileData, interest_in_group_private_package: e.target.value})}
              >
                <option value="">Select...</option>
                <option value="group">Group</option>
                <option value="private">Private</option>
                <option value="both">Both</option>
                <option value="neither">Neither</option>
              </select>
            </div>
            <div className="form-group">
              <label>Music/Ambiance Preference</label>
              <input
                type="text"
                value={profileData.music_ambiance_preference}
                onChange={(e) => setProfileData({...profileData, music_ambiance_preference: e.target.value})}
              />
            </div>
          </div>

          <div className="form-row">
            <div className="form-group">
              <label>Allergies</label>
              <input
                type="text"
                value={profileData.allergies}
                onChange={(e) => setProfileData({...profileData, allergies: e.target.value})}
              />
            </div>
            <div className="form-group">
              <label>Dietary Restrictions</label>
              <input
                type="text"
                value={profileData.dietary_restrictions}
                onChange={(e) => setProfileData({...profileData, dietary_restrictions: e.target.value})}
              />
            </div>
          </div>

          <div className="form-row">
            <div className="form-group">
              <label>Celebration Budget</label>
              <select
                value={profileData.celebration_budget}
                onChange={(e) => setProfileData({...profileData, celebration_budget: e.target.value})}
              >
                <option value="">Select...</option>
                <option value="under_50">Under $50</option>
                <option value="50_100">$50 - $100</option>
                <option value="100_200">$100 - $200</option>
                <option value="200_plus">$200+</option>
              </select>
            </div>
            <div className="form-group">
              <label>Group Size/Solo</label>
              <select
                value={profileData.group_size_solo}
                onChange={(e) => setProfileData({...profileData, group_size_solo: e.target.value})}
              >
                <option value="">Select...</option>
                <option value="solo">Solo</option>
                <option value="2_4">2-4 people</option>
                <option value="5_10">5-10 people</option>
                <option value="10_plus">10+ people</option>
              </select>
            </div>
          </div>

          <div className="form-row">
            <div className="form-group">
              <label>Preferred Contact Method</label>
              <select
                value={profileData.preferred_contact_method}
                onChange={(e) => setProfileData({...profileData, preferred_contact_method: e.target.value})}
              >
                <option value="">Select...</option>
                <option value="email">Email</option>
                <option value="phone">Phone</option>
                <option value="text">Text</option>
                <option value="whatsapp">WhatsApp</option>
              </select>
            </div>
            <div className="form-group">
              <label>Preferred Celebration Style</label>
              <input
                type="text"
                value={profileData.preferred_celebration_style}
                onChange={(e) => setProfileData({...profileData, preferred_celebration_style: e.target.value})}
              />
            </div>
          </div>

          <div className="form-group">
            <label>Personalized Bistro Birthday Treats</label>
            <textarea
              value={profileData.personalized_bistro_birthday_treats}
              onChange={(e) => setProfileData({...profileData, personalized_bistro_birthday_treats: e.target.value})}
              rows="3"
            />
          </div>

          <div className="checkbox-group">
            <label>
              <input
                type="checkbox"
                checked={profileData.want_corporate_offers}
                onChange={(e) => setProfileData({...profileData, want_corporate_offers: e.target.checked})}
              />
              Want Corporate Offers
            </label>
            <label>
              <input
                type="checkbox"
                checked={profileData.interest_in_rewards}
                onChange={(e) => setProfileData({...profileData, interest_in_rewards: e.target.checked})}
              />
              Interest in Rewards
            </label>
            <label>
              <input
                type="checkbox"
                checked={profileData.i_like_surprises}
                onChange={(e) => setProfileData({...profileData, i_like_surprises: e.target.checked})}
              />
              I Like Surprises
            </label>
          </div>

          <div className="form-group">
            <label>Special Notes</label>
            <textarea
              value={profileData.special_notes}
              onChange={(e) => setProfileData({...profileData, special_notes: e.target.value})}
              rows="4"
            />
          </div>

          <button type="submit" disabled={loading || !accountNumber} className="submit-btn">
            {loading ? 'Completing Profile...' : 'Complete Profile'}
          </button>
        </form>
      </div>
    );
  };

  // Dashboard view
  const Dashboard = () => (
    <div className="dashboard">
      <h2>📊 Birthday Club Dashboard</h2>
      
      <div className="stats-grid">
        <div className="stat-card">
          <h3>Total Customers</h3>
          <p className="stat-number">{stats.total_customers || 0}</p>
        </div>
        <div className="stat-card">
          <h3>Subscription</h3>
          <p className="stat-number">{stats.subscription_customers || 0}</p>
        </div>
        <div className="stat-card">
          <h3>Non-Subscription</h3>
          <p className="stat-number">{stats.non_subscription_customers || 0}</p>
        </div>
        <div className="stat-card">
          <h3>Corporate</h3>
          <p className="stat-number">{stats.corporate_customers || 0}</p>
        </div>
        <div className="stat-card">
          <h3>Completed Profiles</h3>
          <p className="stat-number">{stats.completed_profiles || 0}</p>
        </div>
        <div className="stat-card">
          <h3>Profile Completion Rate</h3>
          <p className="stat-number">{Math.round(stats.profile_completion_rate || 0)}%</p>
        </div>
      </div>

      <div className="customers-table">
        <h3>Recent Customers</h3>
        {customers.length === 0 ? (
          <p>No customers yet. Start by adding your first customer!</p>
        ) : (
          <table>
            <thead>
              <tr>
                <th>Account Number</th>
                <th>Name</th>
                <th>Email</th>
                <th>Customer Type</th>
                <th>Profile Status</th>
                <th>Date Joined</th>
              </tr>
            </thead>
            <tbody>
              {customers.map((customer) => (
                <tr key={customer.id}>
                  <td>{customer.account_number}</td>
                  <td>{customer.name}</td>
                  <td>{customer.email}</td>
                  <td className={`type-${customer.customer_type}`}>
                    {customer.customer_type.replace('_', ' ')}
                  </td>
                  <td>
                    <span className={`status ${customer.profile_completed ? 'completed' : 'pending'}`}>
                      {customer.profile_completed ? '✅ Completed' : '⏳ Pending'}
                    </span>
                  </td>
                  <td>{new Date(customer.created_at).toLocaleDateString()}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );

  return (
    <div className="App">
      <header className="header">
        <h1>🎂 Birthday Club Management</h1>
        <nav>
          <button
            className={currentView === 'dashboard' ? 'active' : ''}
            onClick={() => setCurrentView('dashboard')}
          >
            Dashboard
          </button>
          <button
            className={currentView === 'signup' ? 'active' : ''}
            onClick={() => setCurrentView('signup')}
          >
            Customer Signup
          </button>
          <button
            className={currentView === 'profile' ? 'active' : ''}
            onClick={() => setCurrentView('profile')}
          >
            Complete Profile
          </button>
        </nav>
      </header>

      <main className="main-content">
        {message && (
          <div className={`message ${message.includes('❌') ? 'error' : 'success'}`}>
            {message}
          </div>
        )}

        {loading && <div className="loading">Loading...</div>}

        {currentView === 'dashboard' && <Dashboard />}
        {currentView === 'signup' && <CustomerSignupForm />}
        {currentView === 'profile' && <CustomerProfileForm />}
      </main>
    </div>
  );
}

export default App;