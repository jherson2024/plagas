CREATE TABLE tipo_accion (
    TipCod SERIAL PRIMARY KEY,
    TipNom VARCHAR(40) UNIQUE NOT NULL,
    TipDes VARCHAR(160),
    TipCla VARCHAR(40),
    TipEstReg CHAR(1)
);

CREATE TABLE plaga (
    PlaCod SERIAL PRIMARY KEY,
    PlaNom VARCHAR(80) UNIQUE NOT NULL,
    PlaTip VARCHAR(40),
    PlaDes VARCHAR(160),
    PlaTraRec VARCHAR(160),
    PlaEstReg CHAR(1)
);

CREATE TABLE permiso (
    PerCod SERIAL PRIMARY KEY,
    PerNom VARCHAR(80) UNIQUE NOT NULL,
    PerDes VARCHAR(120),
    PerEstReg CHAR(1)
);

CREATE TABLE usuario (
    UsuCod SERIAL PRIMARY KEY,
    UsuNom VARCHAR(80) UNIQUE NOT NULL,
    UsuEma VARCHAR(60) UNIQUE NOT NULL,
    UsuNomUsu VARCHAR(60) UNIQUE NOT NULL,
    UsuCon VARCHAR(60) NOT NULL,
    UsuIdiPre VARCHAR(40),
    UsuUrlFotPer VARCHAR(60),
    UsuFecCre DATE NOT NULL,
    UsuEstReg CHAR(1)
);

CREATE TABLE rol (
    RolCod SERIAL PRIMARY KEY,
    RolNom VARCHAR(40) UNIQUE NOT NULL,
    RolDes VARCHAR(160),
    RolEstReg CHAR(1)
);

CREATE TABLE severidad (
    SevCod SERIAL PRIMARY KEY,
    SevNom VARCHAR(40) UNIQUE NOT NULL,
    SevDes VARCHAR(160),
    SevNivRie INTEGER NOT NULL,
    SevEstReg CHAR(1)
);

CREATE TABLE modelo (
    ModCod SERIAL PRIMARY KEY,
    ModNom VARCHAR(80) UNIQUE NOT NULL,
    ModVer VARCHAR(20) NOT NULL,
    ModFecEnt DATE,
    ModPre DOUBLE PRECISION,
    ModDes VARCHAR(160),
    ModTipArq VARCHAR(40),
    ModDatUsa VARCHAR(80),
    ModUltAct DATE,
    ModEstReg CHAR(1)
);

CREATE TABLE niveles_alerta (
    NivCod SERIAL PRIMARY KEY,
    NivNom VARCHAR(40) UNIQUE NOT NULL,
    NivDes VARCHAR(160),
    NivCodi INTEGER UNIQUE NOT NULL,
    NivEstReg CHAR(1)
);

CREATE TABLE fotografia (
    FotCod SERIAL PRIMARY KEY,
    FotPlaCod INT NOT NULL,
    FotUrlIma VARCHAR(160) UNIQUE NOT NULL,
    FotEstReg CHAR(1),
    FOREIGN KEY (FotPlaCod) REFERENCES plaga(PlaCod)
);

CREATE TABLE parcela (
    ParCod SERIAL PRIMARY KEY,
    ParNom VARCHAR(80) UNIQUE NOT NULL,
    ParUbi VARCHAR(130),
    ParDes VARCHAR(160),
    ParUsuCod INT NOT NULL,
    ParFecReg DATE NOT NULL,
    ParEstReg CHAR(1),
    FOREIGN KEY (ParUsuCod) REFERENCES usuario(UsuCod)
);

CREATE TABLE bitacora_usuario (
    BitCod SERIAL PRIMARY KEY,
    BitFecHor DATE UNIQUE NOT NULL,
    BitUsuCod INT NOT NULL,
    BitAcc VARCHAR(100) NOT NULL,
    BitDes VARCHAR(160),
    BitOri VARCHAR(40),
    BitEstReg CHAR(1),
    FOREIGN KEY (BitUsuCod) REFERENCES usuario(UsuCod)
);

CREATE TABLE cambio_contraseña (
    CamCod SERIAL PRIMARY KEY,
    CamUsuCod INT NOT NULL,
    CamFec DATE NOT NULL,
    CamMet VARCHAR(40),
    CamOri VARCHAR(40),
    CamEstReg CHAR(1),
    FOREIGN KEY (CamUsuCod) REFERENCES usuario(UsuCod)
);

CREATE TABLE bloqueo_intentos (
    BloCod SERIAL PRIMARY KEY,
    BloUsuCod INT NOT NULL,
    BloFecBlo DATE NOT NULL,
    BloInt INTEGER NOT NULL,
    BloMot VARCHAR(160),
    BloEstReg CHAR(1),
    FOREIGN KEY (BloUsuCod) REFERENCES usuario(UsuCod)
);

CREATE TABLE permiso_permitido_rol (
    PerCod SERIAL PRIMARY KEY,
    PerRolCod INT NOT NULL,
    PerPerCod INT NOT NULL,
    PerPre BOOLEAN,
    PerEstReg CHAR(1),
    FOREIGN KEY (PerPerCod) REFERENCES permiso(PerCod),
    FOREIGN KEY (PerRolCod) REFERENCES rol(RolCod)
);

CREATE TABLE evaluacion_modelo (
    EvaCod SERIAL PRIMARY KEY,
    EvaModCod INT NOT NULL,
    EvaFecEva DATE NOT NULL,
    EvaMet VARCHAR(40) NOT NULL,
    EvaVal DOUBLE PRECISION NOT NULL,
    EvaCom VARCHAR(160),
    EvaEstReg CHAR(1),
    FOREIGN KEY (EvaModCod) REFERENCES modelo(ModCod)
);

CREATE TABLE analisis (
    AnaCod SERIAL PRIMARY KEY,
    AnaFotCod INT NOT NULL,
    AnaModCod INT NOT NULL,
    AnaFecAna DATE NOT NULL,
    AnaRes VARCHAR(160),
    AnaCon DOUBLE PRECISION,
    AnaObs VARCHAR(160),
    AnaPlaCod INT NOT NULL,
    AnaSevCod INT NOT NULL,
    AnaEstReg CHAR(1),
    FOREIGN KEY (AnaFotCod) REFERENCES fotografia(FotCod),
    FOREIGN KEY (AnaSevCod) REFERENCES severidad(SevCod),
    FOREIGN KEY (AnaPlaCod) REFERENCES plaga(PlaCod),
    FOREIGN KEY (AnaModCod) REFERENCES modelo(ModCod)
);

CREATE TABLE cultivo (
    CulCod SERIAL PRIMARY KEY,
    CulNom VARCHAR(80) UNIQUE NOT NULL,
    CulTip VARCHAR(40),
    CulParCod INT NOT NULL,
    CulFecSie DATE,
    CulFecCos DATE,
    CulPro BOOLEAN,
    CulUrlIma VARCHAR(60),
    CulEstReg CHAR(1),
    FOREIGN KEY (CulParCod) REFERENCES parcela(ParCod)
);

CREATE TABLE sensor (
    SenCod SERIAL PRIMARY KEY,
    SenSer VARCHAR(40) UNIQUE NOT NULL,
    SenTipSen VARCHAR(40),
    SenUniMed VARCHAR(40),
    SenParCod INT NOT NULL,
    SenLat DOUBLE PRECISION NOT NULL,
    SenLon DOUBLE PRECISION NOT NULL,
    SenFecIns DATE NOT NULL,
    SenEstReg CHAR(1),
    FOREIGN KEY (SenParCod) REFERENCES parcela(ParCod)
);

CREATE TABLE historial_sanitario (
    HisCod SERIAL PRIMARY KEY,
    HisParCod INT NOT NULL,
    HisResEve VARCHAR(160),
    HisPlaFre VARCHAR(160),
    HisNumInf INTEGER,
    HisNumTra INTEGER,
    HisEstReg CHAR(1),
    FOREIGN KEY (HisParCod) REFERENCES parcela(ParCod)
);

CREATE TABLE asignacion_rol_usuario (
    AsiCod SERIAL PRIMARY KEY,
    AsiUsuCod INT NOT NULL,
    AsiRolCod INT NOT NULL,
    AsiParCod INT,
    AsiCulCod INT,
    AsiFecAsi DATE NOT NULL,
    AsiEstReg CHAR(1),
    FOREIGN KEY (AsiParCod) REFERENCES parcela(ParCod),
    FOREIGN KEY (AsiCulCod) REFERENCES cultivo(CulCod),
    FOREIGN KEY (AsiUsuCod) REFERENCES usuario(UsuCod),
    FOREIGN KEY (AsiRolCod) REFERENCES rol(RolCod)
);

CREATE TABLE recomendacion (
    RecCod SERIAL PRIMARY KEY,
    RecFec DATE NOT NULL,
    RecParCod INT NOT NULL,
    RecCulCod INT NOT NULL,
    RecDes VARCHAR(200),
    RecUsuCod INT,
    RecModCod INT,
    RecRecUsu VARCHAR(200),
    RecEstReg CHAR(1),
    FOREIGN KEY (RecParCod) REFERENCES parcela(ParCod),
    FOREIGN KEY (RecModCod) REFERENCES modelo(ModCod),
    FOREIGN KEY (RecCulCod) REFERENCES cultivo(CulCod),
    FOREIGN KEY (RecUsuCod) REFERENCES usuario(UsuCod)
);

CREATE TABLE accion_usuario (
    AccCod SERIAL PRIMARY KEY,
    AccUsuCod INT NOT NULL,
    AccParCod INT NOT NULL,
    AccCulCod INT NOT NULL,
    AccFec DATE NOT NULL,
    AccTipAccCod INT NOT NULL,
    AccDesAcc VARCHAR(260) NOT NULL,
    AccRes VARCHAR(160),
    AccFecDelRes DATE,
    AccEstReg CHAR(1),
    FOREIGN KEY (AccTipAccCod) REFERENCES tipo_accion(TipCod),
    FOREIGN KEY (AccParCod) REFERENCES parcela(ParCod),
    FOREIGN KEY (AccCulCod) REFERENCES cultivo(CulCod),
    FOREIGN KEY (AccUsuCod) REFERENCES usuario(UsuCod)
);

CREATE TABLE infestacion_plaga (
    InfCod SERIAL PRIMARY KEY,
    InfParCod INT,
    InfCulCod INT,
    InfPlaCod INT,
    InfFecDet DATE NOT NULL,
    InfSevCod INT NOT NULL,
    InfEstAct VARCHAR(40),
    InfObs VARCHAR(160),
    InfEstReg CHAR(1),
    FOREIGN KEY (InfSevCod) REFERENCES severidad(SevCod),
    FOREIGN KEY (InfPlaCod) REFERENCES plaga(PlaCod),
    FOREIGN KEY (InfParCod) REFERENCES parcela(ParCod),
    FOREIGN KEY (InfCulCod) REFERENCES cultivo(CulCod)
);

CREATE TABLE lectura_sensor (
    LecCod SERIAL PRIMARY KEY,
    LecFecHor DATE UNIQUE NOT NULL,
    LecSenCod INT NOT NULL,
    LecVal DOUBLE PRECISION NOT NULL,
    LecEstReg CHAR(1),
    FOREIGN KEY (LecSenCod) REFERENCES sensor(SenCod)
);

CREATE TABLE imagen_cultivo (
    ImaCod SERIAL PRIMARY KEY,
    ImaFecHor DATE UNIQUE NOT NULL,
    ImaParCod INT NOT NULL,
    ImaCulCod INT NOT NULL,
    ImaUrlIma VARCHAR(160) NOT NULL,
    ImaSenCod INT NOT NULL,
    ImaLat DOUBLE PRECISION NOT NULL,
    ImaLon DOUBLE PRECISION NOT NULL,
    ImaRes VARCHAR(20),
    ImaTipIma VARCHAR(40),
    ImaAnc INTEGER,
    ImaAlt INTEGER,
    ImaEstReg CHAR(1),
    FOREIGN KEY (ImaParCod) REFERENCES parcela(ParCod),
    FOREIGN KEY (ImaSenCod) REFERENCES sensor(SenCod),
    FOREIGN KEY (ImaCulCod) REFERENCES cultivo(CulCod)
);

CREATE TABLE tratamiento_plaga (
    TraCod SERIAL PRIMARY KEY,
    TraInfPlaCod INT NOT NULL,
    TraProUsa VARCHAR(80),
    TraFecApl DATE NOT NULL,
    TraDos VARCHAR(40),
    TraMetApl VARCHAR(40),
    TraUsuCod INT NOT NULL,
    TraRes VARCHAR(160),
    TraObs VARCHAR(160),
    TraEstReg CHAR(1),
    FOREIGN KEY (TraInfPlaCod) REFERENCES infestacion_plaga(InfCod),
    FOREIGN KEY (TraUsuCod) REFERENCES usuario(UsuCod)
);

CREATE TABLE alerta (
    AleCod SERIAL PRIMARY KEY,
    AleFecHor DATE NOT NULL,
    AleLecSenCod INT,
    AleUsuCod INT,
    AleAnaCod INT,
    AleMen VARCHAR(160) NOT NULL,
    AleMedEnv VARCHAR(40),
    AleNivAleCod INT NOT NULL,
    AleEstReg CHAR(1),
    FOREIGN KEY (AleLecSenCod) REFERENCES lectura_sensor(LecCod),
    FOREIGN KEY (AleAnaCod) REFERENCES analisis(AnaCod),
    FOREIGN KEY (AleNivAleCod) REFERENCES niveles_alerta(NivCod),
    FOREIGN KEY (AleUsuCod) REFERENCES usuario(UsuCod)
);

CREATE TABLE alerta_por_plaga (
    AleCod SERIAL PRIMARY KEY,
    AleFecHor DATE NOT NULL,
    AleAnaCod INT,
    AleLecSenCod INT,
    AlePlaCod INT,
    AleCulCod INT,
    AleParCod INT,
    AleUsuCod INT,
    AleSevCod INT NOT NULL,
    AleRecRap VARCHAR(160),
    AleCanEnv VARCHAR(40),
    AleEstReg CHAR(1),
    FOREIGN KEY (AleLecSenCod) REFERENCES lectura_sensor(LecCod),
    FOREIGN KEY (AleAnaCod) REFERENCES analisis(AnaCod),
    FOREIGN KEY (AleSevCod) REFERENCES severidad(SevCod),
    FOREIGN KEY (AlePlaCod) REFERENCES plaga(PlaCod),
    FOREIGN KEY (AleParCod) REFERENCES parcela(ParCod),
    FOREIGN KEY (AleCulCod) REFERENCES cultivo(CulCod),
    FOREIGN KEY (AleUsuCod) REFERENCES usuario(UsuCod)
);
CREATE TABLE evaluacion_tratamiento (
    EvaCod SERIAL PRIMARY KEY,
    EvaTraPlaCod INT NOT NULL,
    EvaFecEva DATE NOT NULL,
    EvaMejObs BOOLEAN,
    EvaSevCod INT,
    EvaIma VARCHAR(255),
    EvaCom VARCHAR(160),
    EvaEstReg CHAR(1),
    FOREIGN KEY (EvaSevCod) REFERENCES severidad(SevCod),
    FOREIGN KEY (EvaTraPlaCod) REFERENCES tratamiento_plaga(TraCod)
);

