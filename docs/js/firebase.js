// docs/js/firebase.js
// Conexão com Firebase Firestore (modular SDK 10.12.0) e camada de fallback offline

let db = null;
let app = null;
let unsubLacunas = null;
let unsubTrilhas = null;
let unsubVagas = null;
let unsubContexto = null;
let unsubInsights = null;

let callbacks = {
  onLacunas: null,
  onTrilhas: null,
  onVagas: null,
  onContexto: null,
  onInsights: null,
  onStatus: null,
};

let dadosOfflineCache = null;
let slugCursoAtual = "tecnico-em-desenvolvimento-de-sistemas";

/** Carrega os dados de demonstração em modo offline */
export async function carregarDadosOffline() {
  if (dadosOfflineCache) return dadosOfflineCache;
  try {
    const res = await fetch("data/demo_payload.json");
    if (res.ok) {
      dadosOfflineCache = await res.json();
      return dadosOfflineCache;
    }
  } catch (e) {
    console.warn("Aviso: Falha ao carregar data/demo_payload.json, usando memória embutida.", e);
  }
  return null;
}

/** Despacha os dados offline para os listeners ativos */
function despacharDadosOffline(slugCurso) {
  if (!dadosOfflineCache) return;

  if (dadosOfflineCache.contexto && dadosOfflineCache.contexto.atual) {
    callbacks.onContexto?.(dadosOfflineCache.contexto.atual);
  }

  if (dadosOfflineCache.lacunas_cursos && dadosOfflineCache.lacunas_cursos[slugCurso]) {
    callbacks.onLacunas?.(dadosOfflineCache.lacunas_cursos[slugCurso]);
  }

  if (dadosOfflineCache.trilhas_sugeridas && dadosOfflineCache.trilhas_sugeridas[slugCurso]) {
    callbacks.onTrilhas?.(dadosOfflineCache.trilhas_sugeridas[slugCurso]);
  }

  if (dadosOfflineCache.vagas_ativas) {
    const listaVagas = Object.values(dadosOfflineCache.vagas_ativas);
    callbacks.onVagas?.(listaVagas);
  }

  if (dadosOfflineCache.insights) {
    const listaInsights = Object.values(dadosOfflineCache.insights);
    callbacks.onInsights?.(listaInsights);
  }

  callbacks.onStatus?.({ conectado: false, modoDemo: true, texto: "Demonstração Offline" });
}

/** Inicializa conexão Firestore ou ativa fallback offline */
export async function inicializarFirebase(cb) {
  callbacks = { ...callbacks, ...cb };
  const config = window.SKILLRADAR_CONFIG;

  const ehConfigExemplo = !config || !config.apiKey || config.apiKey.includes("EXEMPLO");

  if (ehConfigExemplo) {
    console.info("[SkillRadar] Modo demonstração/offline ativo (chave pública não configurada).");
    await carregarDadosOffline();
    despacharDadosOffline(slugCursoAtual);
    return;
  }

  try {
    // Import dinâmico do Firebase Modular SDK 10.12.0
    const { initializeApp } = await import("https://www.gstatic.com/firebasejs/10.12.0/firebase-app.js");
    const {
      getFirestore,
      collection,
      doc,
      onSnapshot,
      addDoc,
      serverTimestamp,
    } = await import("https://www.gstatic.com/firebasejs/10.12.0/firebase-firestore.js");

    app = initializeApp(config);
    db = getFirestore(app);

    // Listener de Contexto Geral
    unsubContexto = onSnapshot(doc(db, "contexto", "atual"), (snap) => {
      if (snap.exists()) {
        callbacks.onContexto?.(snap.data());
      }
    }, (err) => {
      console.warn("Erro no snapshot de contexto:", err);
      ativarFallbackOffline();
    });

    // Listener de Vagas Ativas
    unsubVagas = onSnapshot(collection(db, "vagas_ativas"), (snap) => {
      const vagas = [];
      snap.forEach((d) => vagas.push({ id: d.id, ...d.data() }));
      callbacks.onVagas?.(vagas);
      callbacks.onStatus?.({ conectado: true, modoDemo: false, texto: "Atualizado ao vivo" });
    }, (err) => {
      console.warn("Erro no snapshot de vagas:", err);
      ativarFallbackOffline();
    });

    // Listener de Insights
    unsubInsights = onSnapshot(collection(db, "insights"), (snap) => {
      const insights = [];
      snap.forEach((d) => insights.push({ id: d.id, ...d.data() }));
      callbacks.onInsights?.(insights);
    }, (err) => {
      console.warn("Erro no snapshot de insights:", err);
    });

    conectarCurso(slugCursoAtual, { doc, onSnapshot });

  } catch (err) {
    console.warn("[SkillRadar] Falha ao conectar ao Firebase Web SDK, alternando para dados locais:", err);
    ativarFallbackOffline();
  }
}

async function ativarFallbackOffline() {
  await carregarDadosOffline();
  despacharDadosOffline(slugCursoAtual);
}

/** Troca o curso ativo e religa os snapshots do Firestore ou dados locais */
export async function trocarCurso(novoSlug) {
  slugCursoAtual = novoSlug;

  if (!db) {
    if (!dadosOfflineCache) await carregarDadosOffline();
    despacharDadosOffline(novoSlug);
    return;
  }

  try {
    const { doc, onSnapshot } = await import("https://www.gstatic.com/firebasejs/10.12.0/firebase-firestore.js");
    conectarCurso(novoSlug, { doc, onSnapshot });
  } catch (err) {
    despacharDadosOffline(novoSlug);
  }
}

function conectarCurso(slug, { doc, onSnapshot }) {
  if (unsubLacunas) unsubLacunas();
  if (unsubTrilhas) unsubTrilhas();

  unsubLacunas = onSnapshot(doc(db, "lacunas_cursos", slug), (snap) => {
    if (snap.exists()) {
      callbacks.onLacunas?.(snap.data());
    }
  }, (err) => {
    console.warn(`Erro no snapshot do curso ${slug}:`, err);
    if (dadosOfflineCache?.lacunas_cursos?.[slug]) {
      callbacks.onLacunas?.(dadosOfflineCache.lacunas_cursos[slug]);
    }
  });

  unsubTrilhas = onSnapshot(doc(db, "trilhas_sugeridas", slug), (snap) => {
    if (snap.exists()) {
      callbacks.onTrilhas?.(snap.data());
    }
  }, (err) => {
    console.warn(`Erro no snapshot da trilha ${slug}:`, err);
    if (dadosOfflineCache?.trilhas_sugeridas?.[slug]) {
      callbacks.onTrilhas?.(dadosOfflineCache.trilhas_sugeridas[slug]);
    }
  });
}

/** Grava documento anônimo de perfil do aluno em interesses_alunos */
export async function salvarInteresseAluno(dados) {
  if (db) {
    try {
      const { collection, addDoc, serverTimestamp } = await import(
        "https://www.gstatic.com/firebasejs/10.12.0/firebase-firestore.js"
      );
      await addDoc(collection(db, "interesses_alunos"), {
        curso_interesse: dados.curso_interesse,
        nivel: dados.nivel,
        areas: dados.areas,
        criado_em: serverTimestamp(),
      });
      return { sucesso: true, remoto: true };
    } catch (e) {
      console.warn("Erro ao salvar no Firestore, salvando localmente:", e);
    }
  }

  // Fallback local caso offline ou regras neguem
  try {
    const registros = JSON.parse(localStorage.getItem("skillradar_interesses") || "[]");
    registros.push({ ...dados, criado_em: new Date().toISOString() });
    localStorage.setItem("skillradar_interesses", JSON.stringify(registros));
    return { sucesso: true, remoto: false };
  } catch (e) {
    return { sucesso: false, erro: e.message };
  }
}
