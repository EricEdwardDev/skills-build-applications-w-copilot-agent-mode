import React, { useState, useEffect } from 'react';

function Workouts() {
  const [workouts, setWorkouts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchWorkouts = async () => {
      try {
        const codespaceName = process.env.REACT_APP_CODESPACE_NAME || 'localhost';
        const baseUrl = codespaceName === 'localhost' 
          ? `http://localhost:8000/api/workouts/`
          : `https://${codespaceName}-8000.app.github.dev/api/workouts/`;

        console.log('Fetching workouts from:', baseUrl);

        const response = await fetch(baseUrl);
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        console.log('Raw data received:', data);

        // Handle both paginated (.results) and plain array responses
        const workoutsList = data.results || data;
        console.log('Processed workouts:', workoutsList);

        setWorkouts(Array.isArray(workoutsList) ? workoutsList : []);
        setLoading(false);
      } catch (error) {
        console.error('Error fetching workouts:', error);
        setError(error.message);
        setLoading(false);
      }
    };

    fetchWorkouts();
  }, []);

  if (loading) {
    return (
      <div className="container mt-4">
        <div className="row justify-content-center">
          <div className="col-md-8">
            <div className="alert alert-info" role="alert">
              <div className="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></div>
              <strong>Loading workouts...</strong>
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

  const getTypeColorBadge = (type) => {
    const typeMap = {
      'cardio': 'bg-danger',
      'strength': 'bg-success',
      'flexibility': 'bg-warning',
      'balance': 'bg-info',
    };
    return typeMap[type?.toLowerCase()] || 'bg-secondary';
  };

  return (
    <div className="container mt-5">
      <div className="row">
        <div className="col-12">
          <div className="data-section">
            <div className="section-header">
              <h2 className="mb-0">💪 Workouts</h2>
            </div>
            {workouts.length === 0 ? (
              <div className="empty-state">
                <div className="empty-state-icon">🏋️</div>
                <h5 className="text-muted">No workouts found</h5>
                <p className="text-muted">Workouts will appear once they are created.</p>
              </div>
            ) : (
              <div className="table-responsive">
                <table className="table table-striped table-hover table-bordered">
                  <thead>
                    <tr>
                      <th><strong>ID</strong></th>
                      <th><strong>Name</strong></th>
                      <th><strong>Description</strong></th>
                      <th><strong>Duration</strong></th>
                      <th><strong>Type</strong></th>
                    </tr>
                  </thead>
                  <tbody>
                    {workouts.map((workout) => (
                      <tr key={workout.id}>
                        <td><span className="badge bg-primary">{workout.id}</span></td>
                        <td><strong>{workout.name}</strong></td>
                        <td>{workout.description}</td>
                        <td>
                          <span className="badge bg-secondary">
                            {workout.duration} min
                          </span>
                        </td>
                        <td>
                          <span className={`badge ${getTypeColorBadge(workout.type)}`}>
                            {workout.type}
                          </span>
                        </td>
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

export default Workouts;
