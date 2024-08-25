import { useState} from "react";

import { handleFetch } from "../general/fetch";
import { isValidEmail } from "./validators";
import { AuthStates } from "./auth-form";


export function LoginForm({
    setLoginState,
    setErrorMessage,
    setEmailState,
    setPasswordState,
  }) {
    const [formData, setFormData] = useState({
      email: "",
      password: "",
      rememberMe: false,
    });
    const validEmail = isValidEmail(formData.email);
    const validPassword = formData.password.length > 0;
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
      const options = {
        method: "POST",
        body: JSON.stringify(formData),
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": window.__TOKEN__,
        },
      };
      setIsSending(true);
      const response = await handleFetch("/signin", options, true);
      if (window.__ERROR_STATE__ in response) {
        setErrorMessage(response.error);
      }
      if (window.__SUCCESS_STATE__ in response) {
        window.location.href = "/";
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
        <div className="form-group">
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
        <div className="form-group remember-me">
          <input
            type="checkbox"
            id="remember-me"
            name="rememberMe"
            value={formData.rememberMe}
            onChange={handleChange}
          />
          <label htmlFor="remember-me">Remember me</label>
        </div>
        <div className="form-group submit-container">
          <button type="submit" className="primary-button full-width">
            {!isSending ? "Login" : "loading..."}
          </button>
        </div>
        <div className="account-info-text" style={{ marginTop: "15px" }}>
          Don't have account?{" "}
          <button onClick={() => setLoginState(AuthStates.SIGNUP)}>
            Create a new account
          </button>
        </div>
      </form>
    );
  }
  