"use strict";

const Profile = (function profileIIFE() {
  const Components = (function componentsIIFE() {
    function ProfileContainer({ token, profile }) {
      async function logout() {
        const options = {
          method: "POST",
          credentials: "include",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": token,
          },
        };
        const response = await Base.handleFetch("/logout", options);
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
    return {
      ProfileContainer,
    };
  })();
  return {
    Profile: Components.ProfileContainer,
  };
})();
