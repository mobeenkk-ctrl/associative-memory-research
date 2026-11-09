"""Experimental associative memory engine; standard library only.
Not a neuroscience model or validated improvement over retrieval systems.
"""
from __future__ import annotations
import json, math, re
from dataclasses import dataclass, field
from pathlib import Path

STOP={'the','a','an','is','are','to','of','for','and','or','in','on','at','we','our','with','by','this','that','it','as','from','has','have','be','was','were','what','when','how','who','do','does','i','you'}
def tokens(s): return set(re.findall(r'[a-z0-9]+',s.lower()))-STOP
def overlap(a,b):
    a,b=tokens(a),tokens(b)
    return len(a&b)/max(1,len(a|b))
def clamp(x): return max(0.,min(1.,x))

@dataclass
class Memory:
    id:str
    text:str
    goals:list[str]=field(default_factory=list)
    salience:float=.5
    timestamp:int=0
    use_count:int=0
    last_used:int=0
    links:dict[str,float]=field(default_factory=dict)
    evidence:str='observation'

class AssociativeMemory:
    def __init__(self): self.nodes={}; self.clock=0
    def add(self,id,text,goals=(),salience=.5,evidence='observation'):
        if id in self.nodes: raise ValueError('duplicate memory id')
        self.clock+=1
        node=Memory(id,text,list(goals),clamp(salience),self.clock,evidence=evidence)
        for other in self.nodes.values():
            sim=overlap(text,other.text)
            goal_sim=bool(set(goals)&set(other.goals))
            weight=clamp(.75*sim+(.30 if goal_sim else 0))
            if weight>=.12:
                node.links[other.id]=weight
                other.links[id]=weight
        self.nodes[id]=node
        return node
    def connect(self,a,b,weight,reason='explicit'):
        if a not in self.nodes or b not in self.nodes: raise KeyError('missing memory')
        if a==b: raise ValueError('self link')
        self.nodes[a].links[b]=clamp(weight)
        self.nodes[b].links[a]=clamp(weight)
    def activate(self,query,goal='',top_k=5,spreading=.60,feedback=True):
        self.clock+=1
        base={}
        for id,m in self.nodes.items():
            semantic=overlap(query,m.text)
            goal_match=max([overlap(goal,g) for g in m.goals] or [0.]) if goal else 0.
            recency=math.exp(-.055*(self.clock-m.timestamp))
            utility=min(1.,m.use_count/5.)
            base[id]=(.62*semantic+.20*goal_match+.10*m.salience+.05*recency+.03*utility)
        scores=base.copy()
        for id,m in self.nodes.items():
            denom=sum(m.links.values()) or 1.
            for neighbor,w in m.links.items():
                scores[neighbor]+=spreading*base[id]*w/denom
        ordered=sorted(scores,key=lambda k:(-scores[k],k))[:top_k]
        result=[{'id':id,'text':self.nodes[id].text,'score':round(scores[id],4),
                 'direct':round(base[id],4),'association_gain':round(scores[id]-base[id],4),
                 'evidence':self.nodes[id].evidence} for id in ordered]
        if feedback:
            for id in ordered: self.nodes[id].use_count+=1;self.nodes[id].last_used=self.clock
        return result
    def reinforce(self,a,b,reward=.15):
        old=self.nodes[a].links.get(b,0.)
        self.connect(a,b,old+reward)
    def weaken(self,a,b,penalty=.10):
        old=self.nodes[a].links.get(b,0.)
        self.connect(a,b,old-penalty)
    def save(self,path):
        Path(path).write_text(json.dumps({'clock':self.clock,'nodes':[vars(n) for n in self.nodes.values()]},indent=2))
    @classmethod
    def load(cls,path):
        data=json.loads(Path(path).read_text()); engine=cls();engine.clock=data['clock']
        engine.nodes={n['id']:Memory(**n) for n in data['nodes']}
        return engine
