import { useState, Fragment } from "react";
import { handleFetch } from "../general/fetch";

export function ConfirmForm({ setErrorMessage, email, password }) {
  const [code, setCode] = useState("");
  const validCode = code.length > 0;
  const [isSending, setIsSending] = useState(false);

  const [canResend, setCanResend] = useState(true);

  const handleChange = (e) => {
    const { value } = e.target;
    setCode(value);
  };

  const handleResend = async () => {
    setCanResend(false);
    setTimeout(() => {
      setCanResend(true);
    }, 10000);
    const options = {
      method: "POST",
      body: JSON.stringify({
        email: email,
        password: password,
      }),
      headers: {
        "Content-Type": "application/json",
      },
    };
    const response = await handleFetch(
      window.__ENDPOINT_RESENDCONFIRMATION__,
      options,
      true
    );
    if (window.__ERROR_STATE__ in response) {
      setErrorMessage(response.error);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setErrorMessage("");
    if (!validCode) {
      setErrorMessage("no valid code entered");
      return;
    }
    const options = {
      method: "POST",
      body: JSON.stringify({
        code: code,
        email: email,
        password: password,
      }),
      headers: {
        "Content-Type": "application/json",
      },
    };
    setIsSending(true);
    const response = await handleFetch(
      window.__ENDPOINT_VERIFYEMAIL__,
      options,
      true
    );
    if (window.__ERROR_STATE__ in response) {
      setErrorMessage(response.error);
    }
    if (window.__SUCCESS_STATE__ in response) {
      setErrorMessage("");
      window.location.href = "/";
    }
    setIsSending(false);
  };

  return (
    <Fragment>
      <div className="account-info-text">
        A verification code has been sent to your email address. Please enter it
        below to proceed.
        <button disabled={!canResend} onClick={() => handleResend()}>
          resend
        </button>
      </div>
      <form className="form-auth" onSubmit={handleSubmit}>
        <div className="form-group">
          <input
            type="text"
            id="code"
            name="code"
            className={`form-underline`}
            placeholder="code"
            value={code}
            onChange={handleChange}
            required
          />
        </div>
        <div className="form-group submit-container">
          <button type="submit" className="primary-button full-width">
            {!isSending ? "Enter Code" : "loading..."}
          </button>
        </div>
        <div style={{ height: "15px" }}></div>
      </form>
    </Fragment>
  );
}
