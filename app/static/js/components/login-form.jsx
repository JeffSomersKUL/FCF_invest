"use strict";

const LoginForm = (function loginFormIIFE() {
  const Helpers = (function helpersIIFE() {
    function validEmail(email) {
      const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      return re.test(email);
    }

    return {
      validEmail,
    };
  })();

  const Components = (function componentsIIFE() {
    function ErrorContainer({ message }) {
      const [heightContainer, setHeightContainer] = React.useState("0px");
      const errorRef = React.useRef(null);

      React.useEffect(() => {
        if (errorRef.current) {
          setHeightContainer(errorRef.current.clientHeight);
        }
      }, [message]);

      return (
        <div className="error-container" style={{ height: heightContainer }}>
          <div ref={errorRef}>{message && message}</div>
        </div>
      );
    }

    function LoginForm({ setLoginState, setErrorMessage }) {
      const [formData, setFormData] = React.useState({
        email: "",
        password: "",
        rememberMe: false,
      });
      const validEmail = Helpers.validEmail(formData.email);
      const validPassword = formData.password.length > 0;
      const [isSending, setIsSending] = React.useState(false);

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
            "X-CSRFToken": token,
          },
        };
        setIsSending(true);
        const response = await Base.handleFetch("/signin", options, true);
        if ("error" in response) {
          setErrorMessage(response.error);
        }
        if ("success" in response) {
          window.location.href = "/";
        }
        setIsSending(false);
      };

      return (
        <form onSubmit={handleSubmit}>
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
            {validPassword && (
              <i className="icon-feedback-form bi bi-check"></i>
            )}
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
              {!isSending ? "Login" : "loading"}
            </button>
          </div>
          <div className="account-info-text">
            Don't have account?{" "}
            <b onClick={() => setLoginState(false)}>Create a new account</b>
          </div>
        </form>
      );
    }

    function SignupForm({ setLoginState, setErrorMessage }) {
      const [formData, setFormData] = React.useState({
        firstname: "",
        lastname: "",
        email: "",
        password: "",
        confirmPassword: "",
      });
      const validEmail = Helpers.validEmail(formData.email);
      const validFirstname = formData.firstname.length > 0;
      const validLastName = formData.lastname.length > 0;
      const validPassword = formData.password.length > 0;
      const validConfirmPassword =
        formData.password == formData.confirmPassword &&
        formData.confirmPassword.length > 0;
      const [isSending, setIsSending] = React.useState(false);

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
        if (!validFirstname) {
          setErrorMessage("no first name entered");
          return;
        }
        if (!validLastName) {
          setErrorMessage("no last name entered");
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
            "X-CSRFToken": token,
          },
        };
        setIsSending(true);
        const response = await Base.handleFetch("/signup", options, true);
        if ("error" in response) {
          setErrorMessage(response.error);
        }
        if ("success" in response) {
          window.location.href = "/";
        }
        setIsSending(false);
      };

      return (
        <form onSubmit={handleSubmit}>
          <div className="row-name">
            <div className="col-name">
              <div className="form-group">
                <input
                  type="text"
                  id="firstname"
                  name="firstname"
                  className={`form-underline ${validFirstname && "valid"}`}
                  placeholder="First Name"
                  value={formData.firstname}
                  onChange={handleChange}
                  required
                />
                {validFirstname && (
                  <i className="icon-feedback-form bi bi-check"></i>
                )}
              </div>
            </div>
            <div className="col-name">
              <div className="form-group">
                <input
                  type="text"
                  id="lastname"
                  name="lastname"
                  className={`form-underline ${validLastName && "valid"}`}
                  placeholder="Last Name"
                  value={formData.lastname}
                  onChange={handleChange}
                  required
                />
                {validLastName && (
                  <i className="icon-feedback-form bi bi-check"></i>
                )}
              </div>
            </div>
          </div>
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
            {validPassword && (
              <i className="icon-feedback-form bi bi-check"></i>
            )}
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
              {!isSending ? "Signup" : "loading"}
            </button>
          </div>
          <div className="account-info-text">
            Already have an account?{" "}
            <b onClick={() => setLoginState(true)}>Login</b>
            <br />
            Only members can create an account
          </div>
        </form>
      );
    }

    function Form({ token }) {
      const [loginState, setLoginState] = React.useState(true);
      const [heightForm, setHeighForm] = React.useState("fit-content");
      const formRef = React.useRef(null);

      const [errorMessage, setErrorMessage] = React.useState("");

      React.useEffect(() => {
        if (formRef.current) {
          setHeighForm(formRef.current.clientHeight);
        }
      }, [loginState]);

      React.useEffect(() => {
        setErrorMessage("");
      }, [loginState]);

      return (
        <div className="login-container">
          <div className="login-header">
            <img
              className="login-img"
              src="../static/images/login/transparant-profile.png"
            />
            <div>{loginState ? "Login" : "Signup"}</div>
          </div>
          <div className="form-input-container" style={{ height: heightForm }}>
            <div className="form" ref={formRef}>
              {loginState ? (
                <Components.LoginForm
                  setLoginState={setLoginState}
                  setErrorMessage={setErrorMessage}
                  token={token}
                />
              ) : (
                <Components.SignupForm
                  setLoginState={setLoginState}
                  setErrorMessage={setErrorMessage}
                  token={token}
                />
              )}
            </div>
          </div>
          <ErrorContainer message={errorMessage} />
        </div>
      );
    }

    return {
      Form,
      LoginForm,
      SignupForm,
    };
  })();
  return { LoginForm: Components.Form };
})();
