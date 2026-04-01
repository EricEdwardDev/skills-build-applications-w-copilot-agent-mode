import React, { useState, useEffect } from 'react';

function Activities() {
  const [activities, setActivities] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchActivities = async () => {
      try {
        const codespaceName = process.env.REACT_APP_CODESPACE_NAME || 'localhost';
        const baseUrl = codespaceName === 'localhost' 
          ? `http://localhost:8000/api/activities/`
          : `https://${codespaceName}-8000.app.github.dev/api/activities/`;

        console.log('Fetching activities from:', baseUrl);

        const response = await fetch(baseUrl);
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        console.log('Raw data received:', data);

        // Handle both paginated (.results) and plain array responses
        const activityList = data.results || data;
        console.log('Processed activities:', activityList);

        setActivities(Array.isArray(activityList) ? activityList : []);
        setLoading(false);
      } catch (error) {
        console.error('Error fetching activities:', error);
        setError(error.message);
        setLoading(false);
      }
    };

    fetchActivities();
  }, []);

  if (loading) {
    return (
      <div className="container mt-4">
        <div className="row justify-content-center">
          <div className="col-md-8">
            <div className="alert alert-info" role="alert">
              <div className="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></div>
              <strong>Loading activities...</strong>
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
              <h2 className="mb-0">Activities</h2>
            </div>
            {activities.length === 0 ? (
              <div className="empty-state">
                <div className="empty-state-icon">📋</div>
                <h5 className="text-muted">No activities found</h5>
                <p className="text-muted">There are no activities available at the moment.</p>
              </div>
            ) : (
              <div className="table-responsive">
                <table className="table table-striped table-hover table-bordered">
                  <thead>
                    <tr>
                      <th><strong>ID</strong></th>
                      <th><strong>Name</strong></th>
                      <th><strong>Description</strong></th>
                    </tr>
                  </thead>
                  <tbody>
                    {activities.map((activity) => (
                      <tr key={activity.id}>
                        <td><span className="badge bg-primary">{activity.id}</span></td>
                        <td><strong>{activity.name}</strong></td>
                        <td>{activity.description}</td>
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

export default Activities;
