import { handleFetch } from "../general/fetch";
import { LogOut, Shield } from "lucide-react";

export function ProfileContainer({ profileInfo }) {
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
    <div id="profile-container" className="row">
      <div id="information-container" className="col-lg-4 col-12">
        <div id="profile-screen">
          <div className="actions-container">
            <button
              className="icon-button"
              onClick={() => (window.location.href = window.__ADMIN_URL__)}>
              <Shield size={20} />
            </button>
          </div>
          <div className="info">
            <div className="name-container">
              {profileInfo.firstName} {profileInfo.lastName}
            </div>
            <div className="email-container">{profileInfo.email}</div>
          </div>
          <div className="stock-status">
            <div className="price-status">€2000</div>
            <div className="amount-status">
              ({"X"} amount of stocks at €{"500"})
            </div>
          </div>
          <div className="logout-container">
            <button className="text-button-logout" onClick={logout}>
              <LogOut size={20} />
              logout
            </button>
          </div>
        </div>
      </div>
      <div id="overview-container" className="col-lg-8 col-12 ">
        <div id="overview-screen"></div>
      </div>
      {/* <button className="primary-button" onClick={logout}>
        Admin
      </button>
      <button className="primary-button" onClick={logout}>
        Logout
      </button> */}
    </div>
  );
}
