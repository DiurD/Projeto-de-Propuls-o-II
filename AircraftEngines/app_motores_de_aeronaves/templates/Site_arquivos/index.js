document.addEventListener("DOMContentLoaded", () => {
  const opcoesPrincipais = document.getElementById("opcoes-principais");
  const offDesignRadio = document.getElementById("offDesign");
  const onDesignRadio = document.getElementById("onDesign");

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

    if (motor == "ramjet" && onDesign && ideal) {
      esconderTudo();
      if (absoluto) {
        RamjetCaracteristicasAbsoluto.style.display = "block";
        RamjetOnDesignIdeal.style.display = "block";
      } else if (porcentagem) {
        RamjetCaracteristicasPorcentagem.style.display = "block";
        RamjetOnDesignIdeal.style.display = "block";
      }
    }

    if (motor == "ramjet" && onDesign && naoIdeal) {
      esconderTudo();
      if (absoluto) {
        RamjetCaracteristicasAbsoluto.style.display = "block";
        RamjetOnDesignNaoIdeal.style.display = "block";
      } else if (porcentagem) {
        RamjetCaracteristicasPorcentagem.style.display = "block";
        RamjetOnDesignNaoIdeal.style.display = "block";
      }
    }

    if (motor == "ramjet" && offDesign) {
      esconderTudo();
      if (absoluto) {
        RamjetCaracteristicasAbsoluto.style.display = "block";
        RamjetOffDesign.style.display = "block";
        RamjetOffDesignRef.style.display = "block";
      } else if (porcentagem) {
        RamjetCaracteristicasPorcentagem.style.display = "block";
        RamjetOffDesign.style.display = "block";
        RamjetOffDesignRef.style.display = "block";
      }
    }

    if (motor == "turbojet" && onDesign && ideal) {
      esconderTudo();
      if (absoluto) {
        TurbojetCaracteristicasAbsoluto.style.display = "block";
        TurbojetOnDesignIdeal.style.display = "block";
      } else if (porcentagem) {
        TurbojetCaracteristicasPorcentagem.style.display = "block";
        TurbojetOnDesignIdeal.style.display = "block";
      }
    }

    if (motor == "turbojet" && onDesign && naoIdeal) {
      esconderTudo();
      if (absoluto) {
        TurbojetCaracteristicasAbsoluto.style.display = "block";
        TurbojetOnDesignNaoIdeal.style.display = "block";
      } else if (porcentagem) {
        TurbojetCaracteristicasPorcentagem.style.display = "block";
        TurbojetOnDesignNaoIdeal.style.display = "block";
      }
    }

    if (motor == "turbojet" && offDesign) {
      esconderTudo();
      if (absoluto) {
        TurbojetCaracteristicasAbsoluto.style.display = "block";
        TurbojetOffDesign.style.display = "block";
        TurbojetOffDesignRef.style.display = "block";
      } else if (porcentagem) {
        TurbojetCaracteristicasPorcentagem.style.display = "block";
        TurbojetOffDesign.style.display = "block";
        TurbojetOffDesignRef.style.display = "block";
      }
    }

    if (motor == "turboprop" && onDesign && ideal) {
      esconderTudo();
      if (absoluto) {
        TurbopropCaracteristicasAbsoluto.style.display = "block";
        TurbopropOnDesignIdeal.style.display = "block";
      } else if (porcentagem) {
        TurbopropCaracteristicasPorcentagem.style.display = "block";
        TurbopropOnDesignIdeal.style.display = "block";
      }
    }

    if (motor == "turboprop" && onDesign && naoIdeal) {
      esconderTudo();
      if (absoluto) {
        TurbopropCaracteristicasAbsoluto.style.display = "block";
        TurbopropOnDesignNaoIdeal.style.display = "block";
      } else if (porcentagem) {
        TurbopropCaracteristicasPorcentagem.style.display = "block";
        TurbopropOnDesignNaoIdeal.style.display = "block";
      }
    }

    if (motor == "turboprop" && offDesign) {
      esconderTudo();
      if (absoluto) {
        TurbopropCaracteristicasAbsoluto.style.display = "block";
        TurbopropOffDesign.style.display = "block";
        TurbopropOffDesignRef.style.display = "block";
      } else if (porcentagem) {
        TurbopropCaracteristicasPorcentagem.style.display = "block";
        TurbopropOffDesign.style.display = "block";
        TurbopropOffDesignRef.style.display = "block";
      }
    }

    if (motor == "turbofan" && onDesign && ideal) {
      esconderTudo();
      if (absoluto) {
        TurbofanCaracteristicasAbsoluto.style.display = "block";
        TurbofanOnDesignIdeal.style.display = "block";
      } else if (porcentagem) {
        TurbofanCaracteristicasPorcentagem.style.display = "block";
        TurbofanOnDesignIdeal.style.display = "block";
      }
    }

    if (motor == "turbofan" && onDesign && naoIdeal) {
      esconderTudo();
      if (absoluto) {
        TurbofanCaracteristicasAbsoluto.style.display = "block";
        TurbofanOnDesignNaoIdeal.style.display = "block";
      } else if (porcentagem) {
        TurbofanCaracteristicasPorcentagem.style.display = "block";
        TurbofanOnDesignNaoIdeal.style.display = "block";
      }
    }

    if (motor == "turbofan" && offDesign) {
      esconderTudo();
      if (absoluto) {
        TurbofanCaracteristicasAbsoluto.style.display = "block";
        TurbofanOffDesign.style.display = "block";
        TurbofanOffDesignRef.style.display = "block";
      } else if (porcentagem) {
        TurbofanCaracteristicasPorcentagem.style.display = "block";
        TurbofanOffDesign.style.display = "block";
        TurbofanOffDesignRef.style.display = "block";
      }
    }

    if (motor == "") {
      esconderTudo();
    }
  });

  function esconderTudo() {
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
