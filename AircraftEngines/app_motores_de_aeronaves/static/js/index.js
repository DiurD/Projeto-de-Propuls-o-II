document.addEventListener("DOMContentLoaded", () => {
  const opcoesPrincipais = document.getElementById("opcoes-principais");
  const offDesignRadio = document.getElementById("offDesign");
  const onDesignRadio = document.getElementById("onDesign");
  const botaoCalcular = document.getElementById("Botao-resultados")
  const botaoInserirValores = document.getElementById("botaoInserirValores")
  const menuSection = document.getElementById("motor-menu-section");
  const analiseSection = document.getElementById("analise-modelo-section");
  const tipoAnaliseSection = document.getElementById("tipo-analise-section");
  const valoresSection = document.getElementById("valores-section");
  const opcoesSecundarias = document.getElementById("opcoes-secundarias");


  const RamjetCaracteristicasAbsoluto = document.getElementById(
    "Ramjet-Caracteristicas-absoluto"
  );
  const RamjetCaracteristicasPorcentagem = document.getElementById(
    "Ramjet-Caracteristicas-porcentagem"
  );
  const RamjetOnDesignIdeal = document.getElementById(
    "Ramjet-Parametros-on-design-ideal"
  );
  const RamjetOnDesignNaoIdeal = document.getElementById(
    "Ramjet-Parametros-on-design-nao-ideal"
  );
  const RamjetOffDesign = document.getElementById(
    "Ramjet-Parametros-off-design"
  );
  const RamjetOffDesignRef = document.getElementById(
    "Ramjet-Referencias-off-design"
  );

  const TurbojetCaracteristicasAbsoluto = document.getElementById(
    "Turbojet-Caracteristicas-absoluto"
  );
  const TurbojetCaracteristicasPorcentagem = document.getElementById(
    "Turbojet-Caracteristicas-porcentagem"
  );
  const TurbojetOnDesignIdeal = document.getElementById(
    "Turbojet-Parametros-on-design-ideal"
  );
  const TurbojetOnDesignNaoIdeal = document.getElementById(
    "Turbojet-Parametros-on-design-nao-ideal"
  );
  const TurbojetOffDesign = document.getElementById(
    "Turbojet-Parametros-off-design"
  );
  const TurbojetOffDesignRef = document.getElementById(
    "Turbojet-Referencias-off-design"
  );

  const TurbopropCaracteristicasAbsoluto = document.getElementById(
    "Turboprop-Caracteristicas-absoluto"
  );
  const TurbopropCaracteristicasPorcentagem = document.getElementById(
    "Turboprop-Caracteristicas-porcentagem"
  );
  const TurbopropOnDesignIdeal = document.getElementById(
    "Turboprop-Parametros-on-design-ideal"
  );
  const TurbopropOnDesignNaoIdeal = document.getElementById(
    "Turboprop-Parametros-on-design-nao-ideal"
  );
  const TurbopropOffDesign = document.getElementById(
    "Turboprop-Parametros-off-design"
  );
  const TurbopropOffDesignRef = document.getElementById(
    "Turboprop-Referencias-off-design"
  );

  const TurbofanCaracteristicasAbsoluto = document.getElementById(
    "Turbofan-Caracteristicas-absoluto"
  );
  const TurbofanCaracteristicasPorcentagem = document.getElementById(
    "Turbofan-Caracteristicas-porcentagem"
  );
  const TurbofanOnDesignIdeal = document.getElementById(
    "Turbofan-Parametros-on-design-ideal"
  );
  const TurbofanOnDesignNaoIdeal = document.getElementById(
    "Turbofan-Parametros-on-design-nao-ideal"
  );
  const TurbofanOffDesign = document.getElementById(
    "Turbofan-Parametros-off-design"
  );
  const TurbofanOffDesignRef = document.getElementById(
    "Turbofan-Referencias-off-design"
  );

  offDesignRadio.addEventListener("change", (event) => {
    const checked = event.target.checked;
    const idealOffDesign = document.getElementById("ideal");
    const naoIdealOffDesign = document.getElementById("nao-ideal");

    if (checked) {
      idealOffDesign.disabled = true;
      naoIdealOffDesign.checked = true;
    }
  });

  onDesignRadio.addEventListener("change", (event) => {
    const checked = event.target.checked;
    const idealOffDesign = document.getElementById("ideal");

    if (checked) {
      idealOffDesign.disabled = false;
    }
  });

  opcoesPrincipais.addEventListener("submit", (event) => {
    event.preventDefault();

    const motor = event.target.elements["selecionar-menu"].value;
    const onDesign = event.target.elements["onDesign"].checked;
    const offDesign = event.target.elements["offDesign"].checked;
    const ideal = event.target.elements["ideal"].checked;
    const naoIdeal = event.target.elements["nao-ideal"].checked;
    const absoluto = event.target.elements["absoluto"].checked;
    const porcentagem = event.target.elements["porcentagem"].checked;

    const hiddenInput_motor = document.createElement("input");
    hiddenInput_motor.setAttribute("type", "hidden");
    hiddenInput_motor.setAttribute("name", "motor");
    hiddenInput_motor.setAttribute("value", motor);

    const hiddenInput_onDesign = document.createElement("input");
    hiddenInput_onDesign.setAttribute("type", "hidden");
    hiddenInput_onDesign.setAttribute("name", "onDesign");
    if (onDesign) {
      hiddenInput_onDesign.setAttribute("value", onDesign);
    } else {
      hiddenInput_onDesign.setAttribute("value", offDesign);
    }

    const hiddenInput_ideal = document.createElement("input");
    hiddenInput_ideal.setAttribute("type", "hidden");
    hiddenInput_ideal.setAttribute("name", "ideal");
    if (ideal) {
      hiddenInput_ideal.setAttribute("value", ideal);
    } else {
      hiddenInput_ideal.setAttribute("value", naoIdeal);
    }

    const hiddenInput_absoluto = document.createElement("input");
    hiddenInput_absoluto.setAttribute("type", "hidden");
    hiddenInput_absoluto.setAttribute("name", "absoluto");
    if (absoluto) {
      hiddenInput_absoluto.setAttribute("value", absoluto);
    } else {
      hiddenInput_absoluto.setAttribute("value", porcentagem);
    }

    opcoesSecundarias.appendChild(hiddenInput_motor);
    opcoesSecundarias.appendChild(hiddenInput_onDesign);
    opcoesSecundarias.appendChild(hiddenInput_ideal);
    opcoesSecundarias.appendChild(hiddenInput_absoluto);

    if (motor == "ramjet" && onDesign && ideal) {
      esconderTudo();
      esconderMenuInicial();
      if (absoluto) {
        RamjetCaracteristicasAbsoluto.style.display = "block";
        RamjetOnDesignIdeal.style.display = "block";
        botaoCalcular.style.display = "block";
      } else if (porcentagem) {
        RamjetCaracteristicasPorcentagem.style.display = "block";
        RamjetOnDesignIdeal.style.display = "block";
        botaoCalcular.style.display = "block";
      }
    }

    if (motor == "ramjet" && onDesign && naoIdeal) {
      esconderTudo();
      esconderMenuInicial();
      if (absoluto) {
        RamjetCaracteristicasAbsoluto.style.display = "block";
        RamjetOnDesignNaoIdeal.style.display = "block";
        botaoCalcular.style.display = "block";
      } else if (porcentagem) {
        RamjetCaracteristicasPorcentagem.style.display = "block";
        RamjetOnDesignNaoIdeal.style.display = "block";
        botaoCalcular.style.display = "block";
      }
    }

    if (motor == "ramjet" && offDesign) {
      esconderTudo();
      esconderMenuInicial();
      if (absoluto) {
        RamjetCaracteristicasAbsoluto.style.display = "block";
        RamjetOffDesign.style.display = "block";
        RamjetOffDesignRef.style.display = "block";
        botaoCalcular.style.display = "block";
      } else if (porcentagem) {
        RamjetCaracteristicasPorcentagem.style.display = "block";
        RamjetOffDesign.style.display = "block";
        RamjetOffDesignRef.style.display = "block";
        botaoCalcular.style.display = "block";
      }
    }

    if (motor == "turbojet" && onDesign && ideal) {
      esconderTudo();
      esconderMenuInicial();
      if (absoluto) {
        TurbojetCaracteristicasAbsoluto.style.display = "block";
        TurbojetOnDesignIdeal.style.display = "block";
        botaoCalcular.style.display = "block";
      } else if (porcentagem) {
        TurbojetCaracteristicasPorcentagem.style.display = "block";
        TurbojetOnDesignIdeal.style.display = "block";
        botaoCalcular.style.display = "block";
      }
    }

    if (motor == "turbojet" && onDesign && naoIdeal) {
      esconderTudo();
      esconderMenuInicial();
      if (absoluto) {
        TurbojetCaracteristicasAbsoluto.style.display = "block";
        TurbojetOnDesignNaoIdeal.style.display = "block";
        botaoCalcular.style.display = "block";
      } else if (porcentagem) {
        TurbojetCaracteristicasPorcentagem.style.display = "block";
        TurbojetOnDesignNaoIdeal.style.display = "block";
        botaoCalcular.style.display = "block";
      }
    }

    if (motor == "turbojet" && offDesign) {
      esconderTudo();
      esconderMenuInicial();
      if (absoluto) {
        TurbojetCaracteristicasAbsoluto.style.display = "block";
        TurbojetOffDesign.style.display = "block";
        TurbojetOffDesignRef.style.display = "block";
        botaoCalcular.style.display = "block";
      } else if (porcentagem) {
        TurbojetCaracteristicasPorcentagem.style.display = "block";
        TurbojetOffDesign.style.display = "block";
        TurbojetOffDesignRef.style.display = "block";
        botaoCalcular.style.display = "block";
      }
    }

    if (motor == "turboprop" && onDesign && ideal) {
      esconderTudo();
      esconderMenuInicial();
      if (absoluto) {
        TurbopropCaracteristicasAbsoluto.style.display = "block";
        TurbopropOnDesignIdeal.style.display = "block";
        botaoCalcular.style.display = "block";
      } else if (porcentagem) {
        TurbopropCaracteristicasPorcentagem.style.display = "block";
        TurbopropOnDesignIdeal.style.display = "block";
        botaoCalcular.style.display = "block";
      }
    }

    if (motor == "turboprop" && onDesign && naoIdeal) {
      esconderTudo();
      esconderMenuInicial();
      if (absoluto) {
        TurbopropCaracteristicasAbsoluto.style.display = "block";
        TurbopropOnDesignNaoIdeal.style.display = "block";
        botaoCalcular.style.display = "block";
      } else if (porcentagem) {
        TurbopropCaracteristicasPorcentagem.style.display = "block";
        TurbopropOnDesignNaoIdeal.style.display = "block";
        botaoCalcular.style.display = "block";
      }
    }

    if (motor == "turboprop" && offDesign) {
      esconderTudo();
      esconderMenuInicial();
      if (absoluto) {
        TurbopropCaracteristicasAbsoluto.style.display = "block";
        TurbopropOffDesign.style.display = "block";
        TurbopropOffDesignRef.style.display = "block";
        botaoCalcular.style.display = "block";
      } else if (porcentagem) {
        TurbopropCaracteristicasPorcentagem.style.display = "block";
        TurbopropOffDesign.style.display = "block";
        TurbopropOffDesignRef.style.display = "block";
        botaoCalcular.style.display = "block";
      }
    }

    if (motor == "turbofan" && onDesign && ideal) {
      esconderTudo();
      esconderMenuInicial();
      if (absoluto) {
        TurbofanCaracteristicasAbsoluto.style.display = "block";
        TurbofanOnDesignIdeal.style.display = "block";
        botaoCalcular.style.display = "block";
      } else if (porcentagem) {
        TurbofanCaracteristicasPorcentagem.style.display = "block";
        TurbofanOnDesignIdeal.style.display = "block";
        botaoCalcular.style.display = "block";
      }
    }

    if (motor == "turbofan" && onDesign && naoIdeal) {
      esconderTudo();
      esconderMenuInicial();
      if (absoluto) {
        TurbofanCaracteristicasAbsoluto.style.display = "block";
        TurbofanOnDesignNaoIdeal.style.display = "block";
        botaoCalcular.style.display = "block";
      } else if (porcentagem) {
        TurbofanCaracteristicasPorcentagem.style.display = "block";
        TurbofanOnDesignNaoIdeal.style.display = "block";
        botaoCalcular.style.display = "block";
      }
    }

    if (motor == "turbofan" && offDesign) {
      esconderTudo();
      esconderMenuInicial();
      if (absoluto) {
        TurbofanCaracteristicasAbsoluto.style.display = "block";
        TurbofanOffDesign.style.display = "block";
        TurbofanOffDesignRef.style.display = "block";
        botaoCalcular.style.display = "block";
      } else if (porcentagem) {
        TurbofanCaracteristicasPorcentagem.style.display = "block";
        TurbofanOffDesign.style.display = "block";
        TurbofanOffDesignRef.style.display = "block";
        botaoCalcular.style.display = "block";
      }
    }

    if (motor == "") {
      esconderTudo();
    }
  });


  function esconderMenuInicial() {
    menuSection.style.display = "none";
    analiseSection.style.display = "none";
    tipoAnaliseSection.style.display = "none";
    valoresSection.style.display = "none";
    botaoInserirValores.style.display = "none";

  }

  function esconderTudo() {
    botaoCalcular.style.display = "none";
    RamjetCaracteristicasAbsoluto.style.display = "none";
    RamjetCaracteristicasPorcentagem.style.display = "none";
    RamjetOnDesignIdeal.style.display = "none";
    RamjetOnDesignNaoIdeal.style.display = "none";
    RamjetOffDesign.style.display = "none";
    RamjetOffDesignRef.style.display = "none";
    TurbojetCaracteristicasAbsoluto.style.display = "none";
    TurbojetCaracteristicasPorcentagem.style.display = "none";
    TurbojetOnDesignIdeal.style.display = "none";
    TurbojetOnDesignNaoIdeal.style.display = "none";
    TurbojetOffDesign.style.display = "none";
    TurbojetOffDesignRef.style.display = "none";
    TurbopropCaracteristicasAbsoluto.style.display = "none";
    TurbopropCaracteristicasPorcentagem.style.display = "none";
    TurbopropOnDesignIdeal.style.display = "none";
    TurbopropOnDesignNaoIdeal.style.display = "none";
    TurbopropOffDesign.style.display = "none";
    TurbopropOffDesignRef.style.display = "none";
    TurbofanCaracteristicasAbsoluto.style.display = "none";
    TurbofanCaracteristicasPorcentagem.style.display = "none";
    TurbofanOnDesignIdeal.style.display = "none";
    TurbofanOnDesignNaoIdeal.style.display = "none";
    TurbofanOffDesign.style.display = "none";
    TurbofanOffDesignRef.style.display = "none";
  }
});
