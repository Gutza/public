---
title: "Plato’s Cave and the Child-God Ontology Modeller"
date: 2025-11-28 10:30:00 +0200
description: "Ontology reasoners are often described as checking whether all axioms and asserted triples are true in “some world”, a phrase that sounds mystical until you see it through Plato’s cave and the astronomer’s view of data as shadows. This essay reframes OWL semantics in terms of projections and possible worlds and introduces the ontology modeller as a fallible child-god who both defines and misdefines the laws of their formal universe, explaining what consistency, entailment and the open-world assumption really mean in practice and why the reasoner’s job is not to discover truth but to enforce the discipline of worlds your axioms and data have made possible."
---

# Plato’s Cave and the Child-God Ontology Modeller

As an ontology modeller, you live between two very different worlds. On one side there is the messy, concrete domain you care about: people and contracts, devices and states, swans and colours, bank transfers and regulations. On the other side there is a reasoner that talks in strangely abstract terms about “possible worlds” and insists on sentences like:

> “All axioms and all asserted triples are true in some world; as long as such a world exists, the knowledge base is consistent, but if no such world exists then the KB is in an inconsistent state.”

At first sight, this sounds unhelpfully mystical. What is this “some world”? Why does everything hinge on its existence? And what, exactly, is your responsibility in all of this? To answer that, it helps to step away from OWL jargon for a moment and walk into a cave.

## Plato’s cave, with better optics

Imagine a group of prisoners chained inside a cave. Behind them lies the real world: people moving, animals passing by, objects being carried back and forth. Between this world and the prisoners there is a bright light, so that the real objects cast moving shadows on the wall the prisoners face. The prisoners, unable to turn their heads, see nothing but these shadows. They never see any actual objects or the light behind them.

Now tweak Plato’s story in one crucial way. Assume that the “projector” between the real world and the cave wall is optically perfect. It never invents an object that is not actually there. It only transforms the three-dimensional world into two-dimensional shadows according to fixed rules: geometry, perspective, occlusion. Given a particular arrangement of objects behind them, there is a determined pattern of shadows in front of them.

The prisoners know only two things: the shadows on the wall, and (if they are clever and patient) the rules of projection that govern those shadows. What they do not have, and will never have, is direct access to the world behind them. They cannot stand up and turn around to check their theories. All their knowledge is mediated by the projection.

This is the key idea to keep: there is a rich reality; there is a projection; and there are cave dwellers who see only the projection and try to reconstruct what that reality might be.

## Astronomers in the cave

Astronomers live in the same story, only with better mathematics. Astronomers do not see galaxies or exoplanets directly. They see streams of photons that have travelled for millions or billions of years, had their wavelengths stretched by cosmic expansion, been bent by gravity near massive objects, scattered by gas, filtered by Earth’s atmosphere, distorted by mirrors and lenses, and finally converted to numbers by detectors. What reaches our instruments is not “the universe” but a projection of it, corrupted and transformed—in predictable, well-understood ways.

The crucial point is that the projection rules are, to a large extent, known. General relativity, electromagnetism, radiative transfer, optics, calibration models: taken together, they form the “optical system” between the real universe and the images and spectra we record.

From the astronomer’s point of view:

* there is some real but unreachable three-dimensional universe “out there”;
* there is a projection mechanism (the laws of physics plus instruments);
* there is the pattern of data we observe.

Given this, an honest astronomer never says, “This is the one true universe.” Instead they say something like: “Whatever the real universe is, it must be one of the theoretical universes that, when passed through these physical laws and instrument models, produces exactly the data we see.” In other words: _there are many possible worlds consistent with the shadows I see, so any one of them could be the real world_, with equal probability.

This is the mindset you need to import into OWL.

## From shadows to triples

Now replace photons with triples. An ontology modeller cares about some real domain: actual persons, actual marriages, actual payments, actual swans. The logic engine never touches the real world directly, it only sees the knowledge base: an ontology and a dataset.

The ontology contains axioms. These say things like “Every Swan is a Bird,” “No Person is both Dead and Alive,” “hasMother is functional,” “every Marriage relates two Persons,” and so on. They are analogue to the laws of physics: structural constraints modellers claim the domain satisfies, expressed in OWL.

The dataset contains asserted triples: concrete statements such as `:alice rdf:type :Swan`, `:alice :hasColour :White`, `:bob :hasMother :carol`. These are the shadows on the wall: particular claims about particular individuals.

From the point of view of formal semantics, a “world” is not fantasy; it is a precise mathematical object. It is some abstract universe of objects together with an assignment that says which of those objects count as Swans, which count as Birds, which pairs are related by `hasMother`, and so on, in such a way that every axiom and every asserted triple in your knowledge base comes out true. Such a structure is called a model or an interpretation of the knowledge base.

Given the axioms and facts, logic looks at the class of all models that satisfy them. This class is the analogue of the family of possible universes compatible with the astronomer’s data. Each model is one candidate way the world might be, if everything you have asserted is correct.

At this point, the awkward sentence becomes less mysterious. When the semantics say, “All axioms and all asserted triples are true in some world,” they are simply stating _from inside of the cave_ that there must exist at least one model — at least one world — in which everything you have asserted in the database can be simultaneously true. If such a world exists, your knowledge base is called consistent. If it does not exist (i.e. if no matter how you assign meanings you inevitably violate some axiom or assertion) then the knowledge base is inconsistent.

Consistency is therefore not an emotional or pragmatic judgement. It is literally the existence of at least one possible "real" world in which all of your axioms and triples hold together without contradiction.

## The reasoner as the cave logician

Imagine that one prisoner in the cave is not just any prisoner but a perfect logician. They know every axiom in your ontology and every asserted triple in your dataset. They also know the official semantic rules that tell them what counts as a model. However, like the other prisoners, they are chained facing the wall, they cannot see the real domain. They have no way to check whether your axioms really match how swans behave in nature, or whether your data about Alice is correct. All they can do is ask:

“Given these axioms and these asserted triples, what must be true in every world that satisfies them?”

In other words, they try to deduce new facts about the real world, starting from a very rigorous interpretation of the axioms and asserted facts in the database, _without constraining the gamut of possible real worlds out there_: given this set of axioms and triples, what else **must** also be true?

For any candidate statement φ — say “Alice is a Bird,” or “Bob has exactly one mother,” or “every Swan is white” — the logician proceeds in two steps. First they consider the entire class of models of the knowledge base, meaning all the worlds in which every axiom and every asserted triple comes out true. Then they check whether φ is true in every one of those worlds.

If φ is true in all of them, the knowledge base is said to entail φ, and the logician is justified in reporting it as a consequence. If there are some models where φ is true and other models where φ is false, then φ is simply not entailed (that's because if we assumed φ was either true or false, we would wrongly constrain the gamut of possible real worlds to a smaller subset that what's actually possible based on what we know from the shadows in front of our eyes).

The important discipline is what they do not do. They never declare φ false just because it is not derivable (not derivable = unknowable from the axioms + known facts). “Not entailed” does not mean “its negation is entailed.” It means “there exist at least two possible worlds compatible with your axioms and facts: one where φ holds, another where φ does not.” This is the open world assumption in action: from inside the cave, absence of proof is not proof of absence.

This is precisely the constraint under which astronomers operate. Failure to detect a planet does not prove that no planet exists; it only proves that no planet exists above certain size and brightness thresholds. Similarly, failure to derive a triple does not prove that its negation holds; it only proves that you have not constrained the space of models tightly enough for its truth value to be fixed.

**The OWL reasoner is that perfect cave logician.** It lives entirely inside the semantics. It takes your knowledge base as given, assumes it is meant to be consistent, and computes what is inevitably true in all its models. It has no idea what the real world looks like; it only knows what the shadows on the wall are allowed to look like according to the rules you have given it.

## Enter the child-god ontology modeller

Now place yourself in the story. Unlike the reasoner, you are not chained facing the wall inside the cave. You have conceptual access to the real domain, the real world. You have some understanding of how marriages actually work in the jurisdiction you care about, how bank accounts behave, which states of a machine are possible, what constraints exist between dates and events, what typical swans look like. You are the one who designs the vocabulary, chooses the axioms, and decides what data to load into the store.

Relative to the reasoner, you are godlike: you create the entire formal universe in which it lives. But you are also child-like: fallible, still learning, occasionally careless. You can easily mis-specify the “laws of physics” in your ontology, or misrepresent what has actually happened in your dataset.

### Frequent errors

There are two main ways you can go wrong.

1. You can **under-constrain the ontology**. In the real world you know that a person cannot be married to themselves, or that an invoice cannot be both fully paid and unpaid, or that in this jurisdiction a marriage always involves exactly two parties. But you omit these facts from your axioms, or only encode them partially. The set of models of your knowledge base then contains many worlds you would never accept as realistic: worlds where self-marriage exists, or marriages with seven participants are perfectly fine. From the reasoner’s point of view, these worlds are valid because nothing in the axioms forbids them. As a result, the reasoner cannot derive consequences you take for granted, such as “everyone in a marriage must have at least one spouse,” because your under-constrained set of axioms permit models where the structure is stranger than you intended.

2. You can also **over-constrain** or **mischaracterise** the domain. Suppose you assert in the ontology that all swans are white. In your head what you really meant was “all swans we have observed in this dataset so far are white.” But OWL does not know about “so far”; it treats your statement as a universal law of the domain. If you never assert a black swan, the knowledge base describes a perfectly consistent fantasy world in which swans are indeed all white. The reasoner is entirely justified in inferring, from “x is a Swan,” that “x is White.” If you later assert a particular swan that is explicitly Black and not White, your axioms and your facts can no longer be satisfied together in any world. No matter how you try to interpret “Swan,” “White,” and “Black,” you will end up violating either the universal white-swan axiom or the data about this particular individual. The class of models (possible worlds) becomes empty; the knowledge base is inconsistent.

In both under- and over-constrained situations, the reasoner is doing exactly what the scientist/perfect cave logician promised to do relative to the knowledge base: when the knowledge base is too weak, it refuses to draw stronger conclusions than the models justify, and when the knowledge base is self-contradictory, it refuses to pretend that contradictions are fine. The responsibility for aligning axioms and data with the actual domain lies with you, not with the reasoner. You are the one who can turn around to look at the _real_ real world, compare the behavior of the formal system with the behavior of the real world, and reevaluate the axioms and/or the facts to return to a consistent state.

## Re-reading the awkward sentence

At this point you can go back to the original phrase and translate it into plain terms.

“All axioms and all asserted triples are true in some world” means: we require that there exists at least one model of the knowledge base, at least one way of assigning meaning to classes, properties and individuals such that every axiom and every asserted triple comes out true. If such a model exists, the knowledge base is consistent. If no such model exists — if your axioms and facts jointly demand the impossible — then the knowledge base is inconsistent.

The rest follows from that. The reasoner implicitly says to you:

“Give me your ontology and your data. I will consider all the possible variations of worlds in which everything you have written is true. If there are none, I will tell you your knowledge base is inconsistent. If there are some, I will treat all of them as equally possible, and I will only report as consequences those statements that are true in all of them.”

The phrase “some world” is not an appeal to a mysterious metaphysical realm; it is a reminder that, for logic, truth in your system is always evaluated relative to models. The existence of at least one such model is the bare minimum needed for your theory not to collapse into contradiction. The knowledge that a statement holds in every such model is what justifies the reasoner in presenting it to you as an entailment.

## How to relate to your dataset and your reasoner

For you as an ontology modeller, the practical implications are clear once you internalise this cave-and-astronomy picture.

First, you stop expecting the reasoner to “discover the truth” about your domain. It does not have a back door to reality. It only has what you give it: axioms and asserted triples. Its job is to enforce the discipline of possible worlds, not to compensate for missing domain knowledge.

Second, you treat “not inferred” as “not forced,” not as “false.” When a triple you expected is not entailed, that is a signal to inspect your axioms and your data: perhaps you have under-constrained the ontology, or perhaps the conclusion was never actually justified by what you wrote down. Conversely, when the reasoner declares inconsistency, that is a signal that somewhere you have asserted mutually incompatible claims, such as “all swans are white” together with an explicitly black swan.

Third, you recognise your own role as the child-god in the story. You are responsible for choosing which aspects of your domain you elevate to the status of axioms, and how carefully you curate the facts that enter the store. The reasoner will enforce whatever world these choices describe, whether or not it resembles the world you thought you were modelling.

Seen this way, the awkward sentence is not a threat or a riddle. It is a compact contract between you and the reasoner: you supply the laws and the shadows; it promises to consider only those worlds where every law and every shadow is true, to reject your theory if no such world exists, and to tell you only what is unavoidable across all surviving worlds. Everything else remains possibility rather than knowledge.

Once you adopt that mental model, OWL reasoners stop looking like black boxes and start looking like what they actually are: very disciplined cave dwellers, doing relentless bookkeeping over the worlds your ontology and dataset have made possible.
