"""
Protocol — Tipos de mensajes y eventos para comunicación entre agentes.

Define el contrato de comunicación del sistema jerárquico:
    AgentMessage  : mensaje genérico entre agentes
    AgentEvent    : evento del ciclo de vida de un agente
    TaskRequest   : solicitud de tarea de macro → micro
    TaskResult    : resultado de tarea de micro → macro
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional


# ======================================================================= #
# ENUMERACIONES                                                            #
# ======================================================================= #

class MessageType(str, Enum):
    TASK_REQUEST = "task_request"
    TASK_RESULT = "task_result"
    STATUS_UPDATE = "status_update"
    ERROR = "error"
    HEARTBEAT = "heartbeat"
    ACTIVATION = "activation"
    DEACTIVATION = "deactivation"


class TaskStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    SUCCESS = "success"
    ERROR = "error"
    SKIPPED = "skipped"


class AgentTier(str, Enum):
    MICRO = "micro"
    MACRO = "macro"


# ======================================================================= #
# DATACLASSES DE MENSAJES                                                  #
# ======================================================================= #

@dataclass
class AgentMessage:
    """
    Mensaje genérico entre dos agentes.

    Attributes:
        sender_id   : identificador del agente que envía
        receiver_id : identificador del agente destinatario (None = broadcast)
        type        : tipo de mensaje (MessageType)
        payload     : datos asociados al mensaje
        message_id  : UUID único generado automáticamente
        timestamp   : momento de creación (UTC ISO 8601)
        correlation_id: para vincular request/response
    """
    sender_id: str
    receiver_id: Optional[str]
    type: MessageType
    payload: Dict[str, Any] = field(default_factory=dict)
    message_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")
    correlation_id: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "message_id": self.message_id,
            "sender_id": self.sender_id,
            "receiver_id": self.receiver_id,
            "type": self.type.value,
            "payload": self.payload,
            "timestamp": self.timestamp,
            "correlation_id": self.correlation_id,
        }


@dataclass
class AgentEvent:
    """
    Evento del ciclo de vida de un agente (registro, error, salud, etc.)

    Attributes:
        agent_id   : agente que genera el evento
        event_type : categoría del evento (str libre)
        data       : detalles del evento
        severity   : "info" | "warning" | "error" | "critical"
    """
    agent_id: str
    event_type: str
    data: Dict[str, Any] = field(default_factory=dict)
    severity: str = "info"
    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "event_id": self.event_id,
            "agent_id": self.agent_id,
            "event_type": self.event_type,
            "data": self.data,
            "severity": self.severity,
            "timestamp": self.timestamp,
        }


@dataclass
class TaskRequest:
    """
    Solicitud de tarea enviada por un agente macro a un agente micro.

    Attributes:
        task_id     : identificador único de la tarea
        intent      : descripción de lo que se debe hacer
        skill_target: nombre del skill/micro-agente destino (None = cualquiera)
        context     : datos/recursos para ejecutar la tarea
        priority    : 1 (alta) … 10 (baja)
        timeout_sec : tiempo máximo de ejecución en segundos
        requester_id: agente macro que origina la solicitud
    """
    intent: str
    skill_target: Optional[str] = None
    context: Dict[str, Any] = field(default_factory=dict)
    priority: int = 5
    timeout_sec: int = 30
    requester_id: str = "macro"
    task_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "task_id": self.task_id,
            "intent": self.intent,
            "skill_target": self.skill_target,
            "context": self.context,
            "priority": self.priority,
            "timeout_sec": self.timeout_sec,
            "requester_id": self.requester_id,
            "created_at": self.created_at,
        }


@dataclass
class TaskResult:
    """
    Resultado de la ejecución de una tarea por un agente micro.

    Attributes:
        task_id    : vincula con el TaskRequest correspondiente
        agent_id   : agente micro que ejecutó
        status     : TaskStatus
        output     : datos producidos por la ejecución
        q_impact   : efecto neto en Q(t)
        error      : mensaje de error (si status == ERROR)
        duration_ms: tiempo de ejecución en milisegundos
    """
    task_id: str
    agent_id: str
    status: TaskStatus
    output: Dict[str, Any] = field(default_factory=dict)
    q_impact: float = 0.0
    error: Optional[str] = None
    duration_ms: int = 0
    completed_at: str = field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "task_id": self.task_id,
            "agent_id": self.agent_id,
            "status": self.status.value,
            "output": self.output,
            "q_impact": self.q_impact,
            "error": self.error,
            "duration_ms": self.duration_ms,
            "completed_at": self.completed_at,
        }

    @property
    def succeeded(self) -> bool:
        return self.status == TaskStatus.SUCCESS


# ======================================================================= #
# HELPERS                                                                  #
# ======================================================================= #

def make_task_request(
    intent: str,
    skill_target: Optional[str] = None,
    context: Optional[Dict[str, Any]] = None,
    priority: int = 5,
    requester_id: str = "macro",
) -> TaskRequest:
    """Helper para crear TaskRequest con valores por defecto."""
    return TaskRequest(
        intent=intent,
        skill_target=skill_target,
        context=context or {},
        priority=priority,
        requester_id=requester_id,
    )


def make_success_result(
    task_id: str,
    agent_id: str,
    output: Dict[str, Any],
    q_impact: float = 0.0,
    duration_ms: int = 0,
) -> TaskResult:
    """Helper para crear TaskResult exitoso."""
    return TaskResult(
        task_id=task_id,
        agent_id=agent_id,
        status=TaskStatus.SUCCESS,
        output=output,
        q_impact=q_impact,
        duration_ms=duration_ms,
    )


def make_error_result(
    task_id: str,
    agent_id: str,
    error: str,
    duration_ms: int = 0,
) -> TaskResult:
    """Helper para crear TaskResult de error."""
    return TaskResult(
        task_id=task_id,
        agent_id=agent_id,
        status=TaskStatus.ERROR,
        error=error,
        duration_ms=duration_ms,
    )
