import React, { useState, useEffect } from 'react';

function Leaderboard() {
  const [leaderboard, setLeaderboard] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchLeaderboard = async () => {
      try {
        const codespaceName = process.env.REACT_APP_CODESPACE_NAME || 'localhost';
        const baseUrl = codespaceName === 'localhost' 
          ? `http://localhost:8000/api/leaderboard/`
          : `https://${codespaceName}-8000.app.github.dev/api/leaderboard/`;

        console.log('Fetching leaderboard from:', baseUrl);

        const response = await fetch(baseUrl);
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        console.log('Raw data received:', data);

        // Handle both paginated (.results) and plain array responses
        const leaderboardList = data.results || data;
        console.log('Processed leaderboard:', leaderboardList);

        setLeaderboard(Array.isArray(leaderboardList) ? leaderboardList : []);
        setLoading(false);
      } catch (error) {
        console.error('Error fetching leaderboard:', error);
        setError(error.message);
        setLoading(false);
      }
    };

    fetchLeaderboard();
  }, []);

  if (loading) {
    return (
      <div className="container mt-4">
        <div className="row justify-content-center">
          <div className="col-md-8">
            <div className="alert alert-info" role="alert">
              <div className="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></div>
              <strong>Loading leaderboard...</strong>
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

  const getRankBadgeColor = (index) => {
    if (index === 0) return 'bg-warning';
    if (index === 1) return 'bg-secondary';
    if (index === 2) return 'bg-danger';
    return 'bg-info';
  };

  return (
    <div className="container mt-5">
      <div className="row">
        <div className="col-12">
          <div className="data-section">
            <div className="section-header">
              <h2 className="mb-0">🏆 Leaderboard</h2>
            </div>
            {leaderboard.length === 0 ? (
              <div className="empty-state">
                <div className="empty-state-icon">📊</div>
                <h5 className="text-muted">No leaderboard data available</h5>
                <p className="text-muted">Start logging activities to see rankings.</p>
              </div>
            ) : (
              <div className="table-responsive">
                <table className="table table-striped table-hover table-bordered">
                  <thead>
                    <tr>
                      <th><strong>Rank</strong></th>
                      <th><strong>User</strong></th>
                      <th><strong>Score</strong></th>
                      <th><strong>Points</strong></th>
                    </tr>
                  </thead>
                  <tbody>
                    {leaderboard.map((entry, index) => (
                      <tr key={entry.id || index}>
                        <td>
                          <span className={`badge ${getRankBadgeColor(index)} fs-6`}>
                            #{index + 1}
                          </span>
                        </td>
                        <td><strong>{entry.user?.username || entry.username || 'N/A'}</strong></td>
                        <td>
                          <span className="badge bg-primary">{entry.score || 0}</span>
                        </td>
                        <td>
                          <span className="badge bg-success">{entry.points || 0} pts</span>
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

export default Leaderboard;
