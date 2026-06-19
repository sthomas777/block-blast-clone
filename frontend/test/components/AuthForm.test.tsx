import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, it, vi } from "vitest";

import AuthForm from "../../src/components/AuthForm";

function setup(overrides: Partial<React.ComponentProps<typeof AuthForm>> = {}) {
  const onLogin = vi.fn();
  const onRegister = vi.fn();
  render(
    <AuthForm
      onLogin={onLogin}
      onRegister={onRegister}
      error={null}
      {...overrides}
    />,
  );
  return { onLogin, onRegister, user: userEvent.setup() };
}

describe("<AuthForm />", () => {
  it("renders username and password inputs and both action buttons", () => {
    setup();
    expect(screen.getByPlaceholderText("Username")).toBeInTheDocument();
    expect(screen.getByPlaceholderText("Password")).toBeInTheDocument();
    expect(screen.getByRole("button", { name: /log in/i })).toBeInTheDocument();
    expect(
      screen.getByRole("button", { name: /register/i }),
    ).toBeInTheDocument();
  });

  it("calls onLogin with the entered values when the login button is clicked", async () => {
    const { onLogin, user } = setup();

    await user.type(screen.getByPlaceholderText("Username"), "test");
    await user.type(screen.getByPlaceholderText("Password"), "supersecret");
    await user.click(screen.getByRole("button", { name: /log in/i }));

    expect(onLogin).toHaveBeenCalledExactlyOnceWith("test", "supersecret");
  });

  it("calls onRegister with the entered values when the register button is clicked", async () => {
    const { onRegister, user } = setup();

    await user.type(screen.getByPlaceholderText("Username"), "test");
    await user.type(screen.getByPlaceholderText("Password"), "supersecret");
    await user.click(screen.getByRole("button", { name: /register/i }));

    expect(onRegister).toHaveBeenCalledExactlyOnceWith("test", "supersecret");
  });

  it("renders the error message when one is provided", () => {
    setup({ error: "Invalid Password or Username" });
    expect(
      screen.getByText("Invalid Password or Username"),
    ).toBeInTheDocument();
  });

  it("does not render an error element when error is null", () => {
    const { container } = render(
      <AuthForm onLogin={vi.fn()} onRegister={vi.fn()} error={null} />,
    );
    expect(container.querySelector("p")).toBeNull();
  });

  it("uses the password input type for the password field", () => {
    setup();
    expect(screen.getByPlaceholderText("Password")).toHaveAttribute(
      "type",
      "password",
    );
  });
});
