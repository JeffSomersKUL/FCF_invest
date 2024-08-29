import { useState, useEffect, useRef } from "react";
import { CircleUserRound, SendHorizontal } from "lucide-react";

import { LoginForm } from "./login-form";
import { ConfirmForm } from "./confirm-form";
import { SignupForm } from "./signup-form";

export const AuthStates = {
  LOGIN: "login",
  SIGNUP: "signup",
  CONFIRM: "confirm",
};

function ErrorContainer({ message }) {
  const [heightContainer, setHeightContainer] = useState("0px");
  const errorRef = useRef(null);

  useEffect(() => {
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

export function Form() {
  const [loginState, setLoginState] = useState(AuthStates.LOGIN);
  const [heightForm, setHeighForm] = useState("fit-content");
  const formRef = useRef(null);

  const [email, setEmailState] = useState("");
  const [password, setPasswordState] = useState("");

  const [errorMessage, setErrorMessage] = useState("");

  useEffect(() => {
    if (formRef.current) {
      setHeighForm(formRef.current.clientHeight);
    }
  }, [loginState]);

  useEffect(() => {
    setErrorMessage("");
  }, [loginState]);

  const renderAuthState = () => {
    switch (loginState) {
      case AuthStates.LOGIN:
        return (
          <LoginForm
            setLoginState={setLoginState}
            setErrorMessage={setErrorMessage}
            setEmailState={setEmailState}
            setPasswordState={setPasswordState}
          />
        );
      case AuthStates.SIGNUP:
        return (
          <SignupForm
            setLoginState={setLoginState}
            setErrorMessage={setErrorMessage}
            setEmailState={setEmailState}
            setPasswordState={setPasswordState}
          />
        );
      case AuthStates.CONFIRM:
        return (
          <ConfirmForm
            setErrorMessage={setErrorMessage}
            password={password}
            email={email}
          />
        );
      default:
        return null;
    }
  };

  return (
    <div className="login-container">
      <div className="login-header">
        {loginState == AuthStates.LOGIN || loginState == AuthStates.SIGNUP ? (
          <CircleUserRound size={120} strokeWidth={2} />
        ) : (
          <SendHorizontal size={120} strokeWidth={2} />
        )}
        <div>
          {loginState == AuthStates.LOGIN && "Login"}
          {loginState == AuthStates.SIGNUP && "Signup"}
          {loginState == AuthStates.CONFIRM && "Verification"}
        </div>
      </div>
      <div className="form-input-container" style={{ height: heightForm }}>
        <div className="form" ref={formRef}>
          {renderAuthState()}
        </div>
      </div>
      <ErrorContainer message={errorMessage} />
    </div>
  );
}
