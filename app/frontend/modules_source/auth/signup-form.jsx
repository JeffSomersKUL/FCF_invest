import { useState } from "react";
import { handleFetch } from "../general/fetch";
import { isValidEmail } from "./validators";
import { AuthStates } from "./auth-form";

export function SignupForm({
  setLoginState,
  setErrorMessage,
  setEmailState,
  setPasswordState,
}) {
  const [formData, setFormData] = useState({
    email: "",
    password: "",
    confirmPassword: "",
  });
  const validEmail = isValidEmail(formData.email);
  const validPassword = formData.password.length > 0;
  const validConfirmPassword =
    formData.password == formData.confirmPassword &&
    formData.confirmPassword.length > 0;
  const [isSending, setIsSending] = useState(false);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setErrorMessage("");
    if (!validEmail) {
      setErrorMessage("no valid email entered");
      return;
    }
    if (!validPassword) {
      setErrorMessage("no password entered");
      return;
    }
    if (!validConfirmPassword) {
      setErrorMessage("passwords don't match");
      return;
    }
    const options = {
      method: "POST",
      body: JSON.stringify(formData),
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": window.__TOKEN__,
      },
    };
    setIsSending(true);
    const response = await handleFetch("/signup", options, true);
    if (window.__ERROR_STATE__ in response) {
      setErrorMessage(response.error);
    }
    if (window.__CONFIRM_STATE__ in response) {
      setErrorMessage("");
      setEmailState(formData.email);
      setPasswordState(formData.password);
      setLoginState(AuthStates.CONFIRM);
    }
    setIsSending(false);
  };

  return (
    <form className="form-auth" onSubmit={handleSubmit}>
      <div className="form-group" id="email-for-sign-up">
        <input
          type="email"
          id="email"
          name="email"
          className={`form-underline ${validEmail && "valid"}`}
          aria-describedby="emailHelp"
          placeholder="Email"
          value={formData.email}
          onChange={handleChange}
          required
        />
        {validEmail && <i className="icon-feedback-form bi bi-check"></i>}
      </div>
      <div className="form-group">
        <input
          type="password"
          id="password"
          name="password"
          className={`form-underline ${validPassword && "valid"}`}
          placeholder="Password"
          value={formData.password}
          onChange={handleChange}
          required
        />
        {validPassword && <i className="icon-feedback-form bi bi-check"></i>}
      </div>
      <div className="form-group">
        <input
          type="password"
          id="confirm-password"
          name="confirmPassword"
          className={`form-underline ${validConfirmPassword && "valid"}`}
          placeholder="Confirm Password"
          value={formData.confirmPassword}
          onChange={handleChange}
          required
        />
        {validConfirmPassword && (
          <i className="icon-feedback-form bi bi-check"></i>
        )}
      </div>
      <div className="form-group submit-container">
        <button type="submit" className="primary-button full-width">
          {!isSending ? "Signup" : "loading..."}
        </button>
      </div>
      <div className="account-info-text" style={{ marginTop: "15px" }}>
        Already have an account?{" "}
        <button onClick={() => setLoginState(AuthStates.LOGIN)}>Login</button>
        <br />
        Only members can create an account
      </div>
    </form>
  );
}
