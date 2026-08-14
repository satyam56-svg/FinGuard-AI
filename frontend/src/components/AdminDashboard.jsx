import { useCallback, useEffect, useState } from "react";
import {
  getAdminUsers,
  updateUserRole,
  updateUserStatus,
} from "../services/api";
import { getCurrentUser } from "../services/auth";
import {
  Users,
//   ShieldCheck,
  UserCheck,
  UserX,
  RotateCw,
  AlertCircle,
  Lock,
} from "lucide-react";

function AdminDashboard() {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [actionLoading, setActionLoading] = useState(null);

  const currentUser = getCurrentUser();

  const loadUsers = useCallback(async () => {
    setLoading(true);
    setError("");

    try {
        const data = await getAdminUsers();
        setUsers(data);
    } catch (err) {
        setError(err.message || "Unable to load users.");
    } finally {
        setLoading(false);
    }
}, []);

  useEffect(() => {
    loadUsers();
  }, [loadUsers]);

  async function handleRoleChange(userId, newRole) {
    setActionLoading(`role-${userId}`);
    setError("");

    try {
      const updatedUser = await updateUserRole(userId, newRole);

      setUsers((previous) =>
        previous.map((user) => (user.id === updatedUser.id ? updatedUser : user))
      );
    } catch (err) {
      setError(err.message || "Unable to update user role.");
    } finally {
      setActionLoading(null);
    }
  }

  async function handleStatusChange(userId, isActive) {
    setActionLoading(`status-${userId}`);
    setError("");

    try {
      const updatedUser = await updateUserStatus(userId, isActive);

      setUsers((previous) =>
        previous.map((user) => (user.id === updatedUser.id ? updatedUser : user))
      );
    } catch (err) {
      setError(err.message || "Unable to update user status.");
    } finally {
      setActionLoading(null);
    }
  }

  if (loading) {
    return (
      <section className="dashboard-card animate-fade-in">
        <div className="section-header">
          <h2>
            <Users size={20} className="text-primary" /> Admin Control Console
          </h2>
        </div>
        <div className="skeleton-box" style={{ height: "120px", marginBottom: "1rem" }} />
      </section>
    );
  }

  return (
    <section className="dashboard-card animate-fade-in">
      <div className="section-header">
        <div>
          <h2>
            <Users size={20} className="text-primary" /> Enterprise Admin Console
          </h2>
          <p>Manage user access privileges, security roles, and account statuses.</p>
        </div>

        <button
          type="button"
          className="secondary-button"
          onClick={loadUsers}
          disabled={loading}
        >
          <RotateCw size={16} /> Refresh
        </button>
      </div>

      {/* Admin KPI Summary */}
      <div className="stats-grid" style={{ marginBottom: "2rem" }}>
        <div className="stat-card">
          <span>Total Registered Users</span>
          <strong>{users.length}</strong>
        </div>

        <div className="stat-card">
          <span style={{ color: "var(--color-success)" }}>Active Accounts</span>
          <strong style={{ color: "var(--color-success)" }}>
            {users.filter((user) => user.is_active).length}
          </strong>
        </div>

        <div className="stat-card">
          <span style={{ color: "var(--color-danger)" }}>Admins</span>
          <strong style={{ color: "var(--color-danger)" }}>
            {users.filter((user) => user.role === "ADMIN").length}
          </strong>
        </div>

        <div className="stat-card">
          <span style={{ color: "var(--color-warning)" }}>Analysts</span>
          <strong style={{ color: "var(--color-warning)" }}>
            {users.filter((user) => user.role === "ANALYST").length}
          </strong>
        </div>
      </div>

      {error && (
        <div className="error-card" style={{ marginBottom: "1.5rem" }}>
          <AlertCircle size={18} />
          <span>{error}</span>
        </div>
      )}

      {/* User Management Section */}
      <div className="dashboard-section">
        <h3>User Management & Access Controls</h3>

        <div className="user-list">
          {users.map((user) => {
            const isCurrentAdmin = currentUser?.username === user.username;
            const roleLoading = actionLoading === `role-${user.id}`;
            const statusLoading = actionLoading === `status-${user.id}`;

            return (
              <div className="user-management-card" key={user.id}>
                <div className="user-info">
                  <div style={{ display: "flex", alignItems: "center", gap: "0.5rem" }}>
                    <strong>{user.username}</strong>
                    {isCurrentAdmin && (
                      <span
                        className="status-badge"
                        style={{
                          fontSize: "0.65rem",
                          padding: "0.15rem 0.45rem",
                          backgroundColor: "rgba(59, 130, 246, 0.15)",
                          color: "var(--primary-light)",
                        }}
                      >
                        (You)
                      </span>
                    )}
                  </div>
                  <span>{user.email}</span>
                  <span style={{ fontFamily: "var(--font-mono)", fontSize: "0.75rem", color: "var(--text-muted)" }}>
                    User ID: {user.id}
                  </span>
                </div>

                <div className="user-role" style={{ display: "flex", flexDirection: "column", gap: "0.25rem" }}>
                  <label style={{ fontSize: "0.75rem", color: "var(--text-muted)", fontWeight: 600 }}>
                    ASSIGN ROLE
                  </label>
                  <select
                    value={user.role}
                    disabled={isCurrentAdmin || roleLoading}
                    onChange={(event) => handleRoleChange(user.id, event.target.value)}
                  >
                    <option value="USER">USER</option>
                    <option value="ANALYST">ANALYST</option>
                    <option value="ADMIN">ADMIN</option>
                  </select>
                </div>

                <div className="user-status" style={{ display: "flex", flexDirection: "column", gap: "0.25rem" }}>
                  <span style={{ fontSize: "0.75rem", color: "var(--text-muted)", fontWeight: 600 }}>
                    ACCOUNT STATUS
                  </span>
                  <div>
                    <span
                      className={`user-status-badge ${
                        user.is_active ? "active" : "inactive"
                      }`}
                    >
                      {user.is_active ? "ACTIVE" : "INACTIVE"}
                    </span>
                  </div>
                </div>

                <div className="user-actions">
                  <button
                    type="button"
                    className="secondary-button"
                    disabled={isCurrentAdmin || statusLoading}
                    onClick={() => handleStatusChange(user.id, !user.is_active)}
                  >
                    {isCurrentAdmin ? (
                      <>
                        <Lock size={14} /> Self Protected
                      </>
                    ) : statusLoading ? (
                      "Updating..."
                    ) : user.is_active ? (
                      <>
                        <UserX size={14} /> Deactivate
                      </>
                    ) : (
                      <>
                        <UserCheck size={14} /> Activate
                      </>
                    )}
                  </button>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
}

export default AdminDashboard;