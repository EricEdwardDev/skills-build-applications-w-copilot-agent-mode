import React, { useState, useEffect } from 'react';

function Users() {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchUsers = async () => {
      try {
        const codespaceName = process.env.REACT_APP_CODESPACE_NAME || 'localhost';
        const baseUrl = codespaceName === 'localhost' 
          ? `http://localhost:8000/api/users/`
          : `https://${codespaceName}-8000.app.github.dev/api/users/`;

        console.log('Fetching users from:', baseUrl);

        const response = await fetch(baseUrl);
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        console.log('Raw data received:', data);

        // Handle both paginated (.results) and plain array responses
        const usersList = data.results || data;
        console.log('Processed users:', usersList);

        setUsers(Array.isArray(usersList) ? usersList : []);
        setLoading(false);
      } catch (error) {
        console.error('Error fetching users:', error);
        setError(error.message);
        setLoading(false);
      }
    };

    fetchUsers();
  }, []);

  if (loading) {
    return (
      <div className="container mt-4">
        <div className="row justify-content-center">
          <div className="col-md-8">
            <div className="alert alert-info" role="alert">
              <div className="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></div>
              <strong>Loading users...</strong>
            </div>
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="container mt-4">
        <div className="row justify-content-center">
          <div className="col-md-8">
            <div className="alert alert-danger" role="alert">
              <strong>Error:</strong> {error}
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="container mt-5">
      <div className="row">
        <div className="col-12">
          <div className="data-section">
            <div className="section-header">
              <h2 className="mb-0">👤 Users</h2>
            </div>
            {users.length === 0 ? (
              <div className="empty-state">
                <div className="empty-state-icon">🔍</div>
                <h5 className="text-muted">No users found</h5>
                <p className="text-muted">Users will appear once they register.</p>
              </div>
            ) : (
              <div className="table-responsive">
                <table className="table table-striped table-hover table-bordered">
                  <thead>
                    <tr>
                      <th><strong>ID</strong></th>
                      <th><strong>Username</strong></th>
                      <th><strong>Email</strong></th>
                      <th><strong>First Name</strong></th>
                      <th><strong>Last Name</strong></th>
                    </tr>
                  </thead>
                  <tbody>
                    {users.map((user) => (
                      <tr key={user.id}>
                        <td><span className="badge bg-primary">{user.id}</span></td>
                        <td><strong>{user.username}</strong></td>
                        <td><a href={`mailto:${user.email}`}>{user.email}</a></td>
                        <td>{user.first_name}</td>
                        <td>{user.last_name}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default Users;
