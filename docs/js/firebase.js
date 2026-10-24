// docs/js/firebase.js
// Conexão com Firebase Firestore (modular SDK 10.12.0) e camada de resiliência com dados embutidos

import { DEMO_PAYLOAD } from "./demo-data.js";

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

let slugCursoAtual = "tecnico-em-desenvolvimento-de-sistemas";

/** Carrega os dados de demonstração embutidos ou de arquivo */
export function carregarDadosOffline() {
  return DEMO_PAYLOAD;
}

/** Despacha os dados determinísticos do payload para a interface */
export function despacharDadosOffline(slugCurso) {
  const dados = DEMO_PAYLOAD;
  if (!dados) return;

  if (dados.contexto && dados.contexto.atual) {
    callbacks.onContexto?.(dados.contexto.atual);
  }

  if (dados.lacunas_cursos && dados.lacunas_cursos[slugCurso]) {
    callbacks.onLacunas?.(dados.lacunas_cursos[slugCurso]);
  }

  if (dados.trilhas_sugeridas && dados.trilhas_sugeridas[slugCurso]) {
    callbacks.onTrilhas?.(dados.trilhas_sugeridas[slugCurso]);
  }

  if (dados.vagas_ativas) {
    const listaVagas = Array.isArray(dados.vagas_ativas)
      ? dados.vagas_ativas
      : Object.values(dados.vagas_ativas);
    callbacks.onVagas?.(listaVagas);
  }

  if (dados.insights) {
    const listaInsights = Array.isArray(dados.insights)
      ? dados.insights
      : Object.values(dados.insights);
    callbacks.onInsights?.(listaInsights);
  }
}

/** Inicializa conexão Firestore ou ativa fallback com os dados embutidos */
export async function inicializarFirebase(cb) {
  callbacks = { ...callbacks, ...cb };

  // 1. Despacha imediatamente os dados locais para carregamento instantâneo
  despacharDadosOffline(slugCursoAtual);

  const config = window.SKILLRADAR_CONFIG;
  const ehConfigExemplo = !config || !config.apiKey || config.apiKey.includes("EXEMPLO");

  if (ehConfigExemplo) {
    console.info("[SkillRadar] Modo demonstração offline ativo.");
    callbacks.onStatus?.({ conectado: false, modoDemo: true, texto: "Demonstração Offline" });
    return;
  }

  try {
    // 2. Conecta ao Firebase Web SDK 10.12.0
    const { initializeApp } = await import("https://www.gstatic.com/firebasejs/10.12.0/firebase-app.js");
    const {
      getFirestore,
      collection,
      doc,
      onSnapshot,
    } = await import("https://www.gstatic.com/firebasejs/10.12.0/firebase-firestore.js");

    app = initializeApp(config);
    db = getFirestore(app);

    // Listener de Contexto Geral
    unsubContexto = onSnapshot(doc(db, "contexto", "atual"), (snap) => {
      if (snap.exists()) {
        callbacks.onContexto?.(snap.data());
      } else if (DEMO_PAYLOAD.contexto?.atual) {
        callbacks.onContexto?.(DEMO_PAYLOAD.contexto.atual);
      }
    }, (err) => {
      console.warn("Snapshot de contexto indisponível:", err.message);
    });

    // Listener de Vagas Ativas
    unsubVagas = onSnapshot(collection(db, "vagas_ativas"), (snap) => {
      const vagas = [];
      snap.forEach((d) => vagas.push({ id: d.id, ...d.data() }));

      if (vagas.length > 0) {
        callbacks.onVagas?.(vagas);
        callbacks.onStatus?.({ conectado: true, modoDemo: false, texto: "Atualizado ao vivo" });
      } else {
        // Se a coleção na nuvem ainda não foi populada, mantém a base de vagas demo
        const vagasDemo = Object.values(DEMO_PAYLOAD.vagas_ativas || {});
        callbacks.onVagas?.(vagasDemo);
        callbacks.onStatus?.({ conectado: true, modoDemo: true, texto: "Atualizado ao vivo (Base Demo)" });
      }
    }, (err) => {
      console.warn("Snapshot de vagas indisponível, mantendo dados locais:", err.message);
      callbacks.onStatus?.({ conectado: false, modoDemo: true, texto: "Demonstração Offline" });
    });

    // Listener de Insights
    unsubInsights = onSnapshot(collection(db, "insights"), (snap) => {
      const insights = [];
      snap.forEach((d) => insights.push({ id: d.id, ...d.data() }));
      if (insights.length > 0) {
        callbacks.onInsights?.(insights);
      } else if (DEMO_PAYLOAD.insights) {
        callbacks.onInsights?.(Object.values(DEMO_PAYLOAD.insights));
      }
    }, (err) => {
      console.warn("Snapshot de insights indisponível:", err.message);
    });

    conectarCurso(slugCursoAtual, { doc, onSnapshot });

  } catch (err) {
    console.warn("[SkillRadar] Executando com dados determinísticos locais:", err.message);
    callbacks.onStatus?.({ conectado: false, modoDemo: true, texto: "Demonstração Offline" });
  }
}

/** Troca o curso ativo e religa os snapshots do Firestore e dados locais */
export async function trocarCurso(novoSlug) {
  slugCursoAtual = novoSlug;

  // Atualiza imediatamente a visualização com os dados do curso selecionado
  if (DEMO_PAYLOAD.lacunas_cursos?.[novoSlug]) {
    callbacks.onLacunas?.(DEMO_PAYLOAD.lacunas_cursos[novoSlug]);
  }
  if (DEMO_PAYLOAD.trilhas_sugeridas?.[novoSlug]) {
    callbacks.onTrilhas?.(DEMO_PAYLOAD.trilhas_sugeridas[novoSlug]);
  }

  if (!db) return;

  try {
    const { doc, onSnapshot } = await import("https://www.gstatic.com/firebasejs/10.12.0/firebase-firestore.js");
    conectarCurso(novoSlug, { doc, onSnapshot });
  } catch (err) {
    console.warn("Erro ao trocar curso no Firestore:", err.message);
  }
}

function conectarCurso(slug, { doc, onSnapshot }) {
  if (unsubLacunas) unsubLacunas();
  if (unsubTrilhas) unsubTrilhas();

  unsubLacunas = onSnapshot(doc(db, "lacunas_cursos", slug), (snap) => {
    if (snap.exists()) {
      callbacks.onLacunas?.(snap.data());
    } else if (DEMO_PAYLOAD.lacunas_cursos?.[slug]) {
      callbacks.onLacunas?.(DEMO_PAYLOAD.lacunas_cursos[slug]);
    }
  }, (err) => {
    if (DEMO_PAYLOAD.lacunas_cursos?.[slug]) {
      callbacks.onLacunas?.(DEMO_PAYLOAD.lacunas_cursos[slug]);
    }
  });

  unsubTrilhas = onSnapshot(doc(db, "trilhas_sugeridas", slug), (snap) => {
    if (snap.exists()) {
      callbacks.onTrilhas?.(snap.data());
    } else if (DEMO_PAYLOAD.trilhas_sugeridas?.[slug]) {
      callbacks.onTrilhas?.(DEMO_PAYLOAD.trilhas_sugeridas[slug]);
    }
  }, (err) => {
    if (DEMO_PAYLOAD.trilhas_sugeridas?.[slug]) {
      callbacks.onTrilhas?.(DEMO_PAYLOAD.trilhas_sugeridas[slug]);
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
      console.warn("Erro ao salvar no Firestore, salvando localmente:", e.message);
    }
  }

  // Fallback local
  try {
    const registros = JSON.parse(localStorage.getItem("skillradar_interesses") || "[]");
    registros.push({ ...dados, criado_em: new Date().toISOString() });
    localStorage.setItem("skillradar_interesses", JSON.stringify(registros));
    return { sucesso: true, remoto: false };
  } catch (e) {
    return { sucesso: false, erro: e.message };
  }
}
