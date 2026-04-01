import React, { useState, useEffect } from 'react';

function Teams() {
  const [teams, setTeams] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchTeams = async () => {
      try {
        const codespaceName = process.env.REACT_APP_CODESPACE_NAME || 'localhost';
        const baseUrl = codespaceName === 'localhost' 
          ? `http://localhost:8000/api/teams/`
          : `https://${codespaceName}-8000.app.github.dev/api/teams/`;

        console.log('Fetching teams from:', baseUrl);

        const response = await fetch(baseUrl);
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        console.log('Raw data received:', data);

        // Handle both paginated (.results) and plain array responses
        const teamsList = data.results || data;
        console.log('Processed teams:', teamsList);

        setTeams(Array.isArray(teamsList) ? teamsList : []);
        setLoading(false);
      } catch (error) {
        console.error('Error fetching teams:', error);
        setError(error.message);
        setLoading(false);
      }
    };

    fetchTeams();
  }, []);

  if (loading) {
    return (
      <div className="container mt-4">
        <div className="row justify-content-center">
          <div className="col-md-8">
            <div className="alert alert-info" role="alert">
              <div className="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></div>
              <strong>Loading teams...</strong>
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
              <h2 className="mb-0">👥 Teams</h2>
            </div>
            {teams.length === 0 ? (
              <div className="empty-state">
                <div className="empty-state-icon">🏢</div>
                <h5 className="text-muted">No teams found</h5>
                <p className="text-muted">Teams will appear once they are created.</p>
              </div>
            ) : (
              <div className="table-responsive">
                <table className="table table-striped table-hover table-bordered">
                  <thead>
                    <tr>
                      <th><strong>ID</strong></th>
                      <th><strong>Team Name</strong></th>
                      <th><strong>Description</strong></th>
                      <th><strong>Members</strong></th>
                    </tr>
                  </thead>
                  <tbody>
                    {teams.map((team) => (
                      <tr key={team.id}>
                        <td><span className="badge bg-primary">{team.id}</span></td>
                        <td><strong>{team.name}</strong></td>
                        <td>{team.description}</td>
                        <td>
                          <span className="badge bg-info">
                            {team.members?.length || 0} members
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

export default Teams;
