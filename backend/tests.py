from pso import PSO, portfolio_objective, rastrigin_function

if __name__ == "__main__":
    pso_test = PSO(
        num_particles=20,
        num_assets=5,
        returns=[],
        covariance=[],
        iter=2000,
        test=True,
    )
    best_rastrigin = pso_test.optimize()
    print(f"Cel mai bun individ: {best_rastrigin}")
    print(f"Scorul celui mai bun individ: {rastrigin_function(best_rastrigin)}")
    print("Minimul functiei/rezultatul asteptat: 0.0")

    num_assets = 3
    returns = [0.12, 0.10, 0.55]
    covariance = [[0.04, 0.01, 0.02], [0.01, 0.03, 0.01], [0.02, 0.01, 0.05]]
    risk = 1

    pso_test = PSO(
        num_particles=50,
        num_assets=num_assets,
        returns=returns,
        covariance=covariance,
        iter=100,
        test=True,
        risk=risk,
    )

    best_normal = pso_test.optimize()

    print("Actiune cu randament semnificativ mai mare")
    print(f"Cel mai bun individ: {best_normal}")
    print(
        f"Scorul celui mai bun individ: {portfolio_objective(best_normal, returns=returns, covariance=covariance, risk= risk)}"
    )

    num_assets = 3
    returns = [0.10, 0.10, 0.10]
    covariance = [[0.01, 0.01, 0.01], [0.01, 0.01, 0.01], [0.01, 0.01, 0.01]]
    risk = 1

    pso_test = PSO(
        num_particles=50,
        num_assets=num_assets,
        returns=returns,
        covariance=covariance,
        iter=100,
        test=True,
        risk=risk,
    )

    best_normal = pso_test.optimize()

    print("Cel mai rau caz")
    print(f"Cel mai bun individ: {best_normal}")
    print(
        f"Scorul celui mai bun individ: {portfolio_objective(best_normal, returns=returns, covariance=covariance, risk= risk)}"
    )

    num_assets = 3
    returns = [1.64549724, 1.75415578, 23.69861677]
    covariance = [
        [0.1095161, 0.03841349, 0.0840869],
        [0.03841349, 0.03693875, 0.04457163],
        [0.0840869, 0.04457163, 0.11561088],
    ]

    risk = 1000

    pso_test = PSO(
        num_particles=50,
        num_assets=num_assets,
        returns=returns,
        covariance=covariance,
        iter=100,
        test=True,
        risk=risk,
    )

    average = pso_test.optimize()

    print("Caz normal")
    print(f"Cel mai bun individ: {average}")
    print(
        f"Scorul celui mai bun individ: {portfolio_objective(average, returns=returns, covariance=covariance, risk= risk)}"
    )
