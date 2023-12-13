document.addEventListener("DOMContentLoaded", () => {
  const opcoesPrincipais = document.getElementById("opcoes-principais");
  const offDesignRadio = document.getElementById("offDesign");
  const onDesignRadio = document.getElementById("onDesign");
  const botaoCalcular = document.getElementById("Botao-resultados");
  const botaoInserirValores = document.getElementById("botaoInserirValores");
  const menuSection = document.getElementById("motor-menu-section");
  const analiseSection = document.getElementById("analise-modelo-section");
  const tipoAnaliseSection = document.getElementById("tipo-analise-section");
  const valoresSection = document.getElementById("valores-section");
  const opcoesSecundarias = document.getElementById("opcoes-secundarias");
  const botaoVoltar = document.getElementById("botaoVoltar");

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

  function makeRequired(element) {
    const inputs = element.getElementsByTagName("input");
    for (let i = 0; i < inputs.length; i++) {
      inputs[i].required = true;
    }
  }

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
      hiddenInput_onDesign.setAttribute("value", onDesign);
    }

    const hiddenInput_ideal = document.createElement("input");
    hiddenInput_ideal.setAttribute("type", "hidden");
    hiddenInput_ideal.setAttribute("name", "ideal");
    if (ideal) {
      hiddenInput_ideal.setAttribute("value", ideal);
    } else {
      hiddenInput_ideal.setAttribute("value", ideal);
    }

    const hiddenInput_absoluto = document.createElement("input");
    hiddenInput_absoluto.setAttribute("type", "hidden");
    hiddenInput_absoluto.setAttribute("name", "absoluto");
    if (absoluto) {
      hiddenInput_absoluto.setAttribute("value", absoluto);
    } else {
      hiddenInput_absoluto.setAttribute("value", absoluto);
    }

    opcoesSecundarias.appendChild(hiddenInput_motor);
    opcoesSecundarias.appendChild(hiddenInput_onDesign);
    opcoesSecundarias.appendChild(hiddenInput_ideal);
    opcoesSecundarias.appendChild(hiddenInput_absoluto);

    botaoVoltar.style.display = "block";

    if (motor == "ramjet" && onDesign && ideal) {
      esconderTudo();
      esconderMenuInicial();
      if (absoluto) {
        RamjetCaracteristicasAbsoluto.style.display = "block";
        //makeRequired(RamjetCaracteristicasAbsoluto)
        RamjetOnDesignIdeal.style.display = "block";
        //makeRequired(RamjetOnDesignIdeal);
        botaoCalcular.style.display = "block";
      } else if (porcentagem) {
        RamjetCaracteristicasPorcentagem.style.display = "block";
        //makeRequired(RamjetCaracteristicasPorcentagem);
        RamjetOnDesignIdeal.style.display = "block";
        //makeRequired(RamjetOnDesignIdeal);
        botaoCalcular.style.display = "block";
      }
    }

    if (motor == "ramjet" && onDesign && naoIdeal) {
      esconderTudo();
      esconderMenuInicial();
      if (absoluto) {
        RamjetCaracteristicasAbsoluto.style.display = "block";
        //makeRequired(RamjetCaracteristicasAbsoluto);
        RamjetOnDesignNaoIdeal.style.display = "block";
        //makeRequired(RamjetOnDesignNaoIdeal);
        botaoCalcular.style.display = "block";
      } else if (porcentagem) {
        RamjetCaracteristicasPorcentagem.style.display = "block";
        //makeRequired(RamjetCaracteristicasPorcentagem);
        RamjetOnDesignNaoIdeal.style.display = "block";
        //makeRequired(RamjetOnDesignNaoIdeal);
        botaoCalcular.style.display = "block";
      }
    }

    if (motor == "ramjet" && offDesign) {
      esconderTudo();
      esconderMenuInicial();
      if (absoluto) {
        RamjetCaracteristicasAbsoluto.style.display = "block";
        //makeRequired(RamjetCaracteristicasAbsoluto);
        RamjetOffDesign.style.display = "block";
        //makeRequired(RamjetOffDesign);
        RamjetOffDesignRef.style.display = "block";
        //makeRequired(RamjetOffDesignRef);
        botaoCalcular.style.display = "block";
      } else if (porcentagem) {
        RamjetCaracteristicasPorcentagem.style.display = "block";
        //makeRequired(RamjetCaracteristicasPorcentagem);
        RamjetOffDesign.style.display = "block";
        //makeRequired(RamjetOffDesign);
        RamjetOffDesignRef.style.display = "block";
        //makeRequired(RamjetOffDesignRef);
        botaoCalcular.style.display = "block";
      }
    }

    if (motor == "turbojet" && onDesign && ideal) {
      esconderTudo();
      esconderMenuInicial();
      if (absoluto) {
        TurbojetCaracteristicasAbsoluto.style.display = "block";
        // makeRequired(TurbojetCaracteristicasAbsoluto);
        TurbojetOnDesignIdeal.style.display = "block";
        //makeRequired(TurbojetOnDesignIdeal);
        botaoCalcular.style.display = "block";
      } else if (porcentagem) {
        TurbojetCaracteristicasPorcentagem.style.display = "block";
        //makeRequired(TurbojetCaracteristicasPorcentagem);
        TurbojetOnDesignIdeal.style.display = "block";
        //makeRequired(TurbojetOnDesignIdeal);
        botaoCalcular.style.display = "block";
      }
    }

    if (motor == "turbojet" && onDesign && naoIdeal) {
      esconderTudo();
      esconderMenuInicial();
      if (absoluto) {
        TurbojetCaracteristicasAbsoluto.style.display = "block";
        //makeRequired(TurbojetCaracteristicasAbsoluto);
        TurbojetOnDesignNaoIdeal.style.display = "block";
        //makeRequired(TurbojetOnDesignNaoIdeal);
        botaoCalcular.style.display = "block";
      } else if (porcentagem) {
        TurbojetCaracteristicasPorcentagem.style.display = "block";
        //makeRequired(TurbojetCaracteristicasPorcentagem);
        TurbojetOnDesignNaoIdeal.style.display = "block";
        //makeRequired(TurbojetOnDesignNaoIdeal);
        botaoCalcular.style.display = "block";
      }
    }

    if (motor == "turbojet" && offDesign) {
      esconderTudo();
      esconderMenuInicial();
      if (absoluto) {
        TurbojetCaracteristicasAbsoluto.style.display = "block";
        //makeRequired(TurbojetCaracteristicasAbsoluto);
        TurbojetOffDesign.style.display = "block";
        //makeRequired(TurbojetOffDesign);
        TurbojetOffDesignRef.style.display = "block";
        //makeRequired(TurbojetOffDesignRef);
        botaoCalcular.style.display = "block";
      } else if (porcentagem) {
        TurbojetCaracteristicasPorcentagem.style.display = "block";
        //makeRequired(TurbojetCaracteristicasPorcentagem);
        TurbojetOffDesign.style.display = "block";
        //makeRequired(TurbojetOffDesign);
        TurbojetOffDesignRef.style.display = "block";
        //makeRequired(TurbojetOffDesignRef);
        botaoCalcular.style.display = "block";
      }
    }

    if (motor == "turboprop" && onDesign && ideal) {
      esconderTudo();
      esconderMenuInicial();
      if (absoluto) {
        TurbopropCaracteristicasAbsoluto.style.display = "block";
        //makeRequired(TurbopropCaracteristicasAbsoluto);
        TurbopropOnDesignIdeal.style.display = "block";
        //makeRequired(TurbopropOnDesignIdeal);
        botaoCalcular.style.display = "block";
      } else if (porcentagem) {
        TurbopropCaracteristicasPorcentagem.style.display = "block";
        //makeRequired(TurbopropCaracteristicasPorcentagem);
        TurbopropOnDesignIdeal.style.display = "block";
        //makeRequired(TurbopropOnDesignIdeal);
        botaoCalcular.style.display = "block";
      }
    }

    if (motor == "turboprop" && onDesign && naoIdeal) {
      esconderTudo();
      esconderMenuInicial();
      if (absoluto) {
        TurbopropCaracteristicasAbsoluto.style.display = "block";
        //makeRequired(TurbopropCaracteristicasAbsoluto);
        TurbopropOnDesignNaoIdeal.style.display = "block";
        //makeRequired(TurbopropOnDesignNaoIdeal);
        botaoCalcular.style.display = "block";
      } else if (porcentagem) {
        TurbopropCaracteristicasPorcentagem.style.display = "block";
        //makeRequired(TurbopropCaracteristicasPorcentagem);
        TurbopropOnDesignNaoIdeal.style.display = "block";
        //makeRequired(TurbopropOnDesignNaoIdeal);
        botaoCalcular.style.display = "block";
      }
    }

    if (motor == "turboprop" && offDesign) {
      esconderTudo();
      esconderMenuInicial();
      if (absoluto) {
        TurbopropCaracteristicasAbsoluto.style.display = "block";
        //makeRequired(TurbopropCaracteristicasAbsoluto);
        TurbopropOffDesign.style.display = "block";
        //makeRequired(TurbopropOffDesign);
        TurbopropOffDesignRef.style.display = "block";
        //makeRequired(TurbopropOffDesignRef);
        botaoCalcular.style.display = "block";
      } else if (porcentagem) {
        TurbopropCaracteristicasPorcentagem.style.display = "block";
        //makeRequired(TurbopropCaracteristicasPorcentagem);
        TurbopropOffDesign.style.display = "block";
        //makeRequired(TurbopropOffDesign);
        TurbopropOffDesignRef.style.display = "block";
        //makeRequired(TurbopropOffDesignRef);
        botaoCalcular.style.display = "block";
      }
    }

    if (motor == "turbofan" && onDesign && ideal) {
      esconderTudo();
      esconderMenuInicial();
      if (absoluto) {
        TurbofanCaracteristicasAbsoluto.style.display = "block";
        //makeRequired(TurbofanCaracteristicasAbsoluto);
        TurbofanOnDesignIdeal.style.display = "block";
        //makeRequired(TurbofanOnDesignIdeal);
        botaoCalcular.style.display = "block";
      } else if (porcentagem) {
        TurbofanCaracteristicasPorcentagem.style.display = "block";
        //makeRequired(TurbofanCaracteristicasPorcentagem);
        TurbofanOnDesignIdeal.style.display = "block";
        //makeRequired(TurbofanOnDesignIdeal);
        botaoCalcular.style.display = "block";
      }
    }

    if (motor == "turbofan" && onDesign && naoIdeal) {
      esconderTudo();
      esconderMenuInicial();
      if (absoluto) {
        TurbofanCaracteristicasAbsoluto.style.display = "block";
        //makeRequired(TurbofanCaracteristicasAbsoluto);
        TurbofanOnDesignNaoIdeal.style.display = "block";
        //makeRequired(TurbofanOnDesignNaoIdeal);
        botaoCalcular.style.display = "block";
      } else if (porcentagem) {
        TurbofanCaracteristicasPorcentagem.style.display = "block";
        //makeRequired(TurbofanCaracteristicasPorcentagem);
        TurbofanOnDesignNaoIdeal.style.display = "block";
        //makeRequired(TurbofanOnDesignNaoIdeal);
        botaoCalcular.style.display = "block";
      }
    }

    if (motor == "turbofan" && offDesign) {
      esconderTudo();
      esconderMenuInicial();
      if (absoluto) {
        TurbofanCaracteristicasAbsoluto.style.display = "block";
        //makeRequired(TurbofanCaracteristicasAbsoluto);
        TurbofanOffDesign.style.display = "block";
        //makeRequired(TurbofanOffDesign);
        TurbofanOffDesignRef.style.display = "block";
        //makeRequired(TurbofanOffDesignRef);
        botaoCalcular.style.display = "block";
      } else if (porcentagem) {
        TurbofanCaracteristicasPorcentagem.style.display = "block";
        //makeRequired(TurbofanCaracteristicasPorcentagem);
        TurbofanOffDesign.style.display = "block";
        //makeRequired(TurbofanOffDesign);
        TurbofanOffDesignRef.style.display = "block";
        //makeRequired(TurbofanOffDesignRef);
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
