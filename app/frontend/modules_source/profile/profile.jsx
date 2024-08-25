import { handleFetch } from "../general/fetch";

export function ProfileContainer() {
  async function logout() {
    const options = {
      method: "POST",
      credentials: "include",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": window.__TOKEN__,
      },
    };
    const response = await handleFetch("/logout", options);
    if ("success" in response) {
      window.location.href = "/login";
    }
  }

  return (
    <div id="profile-container">
      <button className="primary-button" onClick={logout}>
        Admin
      </button>
      <button className="primary-button" onClick={logout}>
        Logout
      </button>
    </div>
  );
}
