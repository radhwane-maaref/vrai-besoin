<template>
  <!-- Full page wrapper centering the content on large screens -->
  <div class="min-h-screen bg-[#F8F6F2] font-['DM_Sans',_sans-serif] flex justify-center">

    <!-- Responsive inner container -->
    <div class="w-full max-w-3xl px-4 sm:px-6 md:px-8 py-6 sm:py-8 lg:py-10">

      <!-- Header Section -->
      <SettingsPageHeader title="Conditions d'utilisation"/>

      <!-- Content Card -->
      <section class="bg-[#FFFFFF] border border-[#D9D9D9] rounded-[20px] sm:rounded-[24px] p-6 sm:p-8 shadow-sm">

        <div class="space-y-6 sm:space-y-8 text-[14px] sm:text-[15px] leading-relaxed text-[#6B7280]">

          <!-- Section 1 -->
          <div>
            <h2 class="text-lg sm:text-xl font-bold text-[#000000] mb-2 sm:mb-3">
              1. Acceptation des conditions
            </h2>
            <p>
              En accédant au site vraibesoin.me et en utilisant les services proposés par Vrai Besoin, vous acceptez
              pleinement et sans réserve les présentes Conditions Générales d'Utilisation. Si vous n'êtes pas en accord
              avec tout ou partie de ces conditions, il vous est fortement recommandé de ne pas utiliser la plateforme.
            </p>
          </div>

          <!-- Section 2 -->
          <div>
            <h2 class="text-lg sm:text-xl font-bold text-[#000000] mb-2 sm:mb-3">
              2. Accès aux services et création de compte
            </h2>
            <p>
              L'accès à certaines fonctionnalités de la plateforme peut nécessiter la création d'un compte utilisateur.
              Vous vous engagez à fournir des informations exactes, complètes et à jour lors de votre inscription. Vous
              êtes seul responsable de la confidentialité de vos identifiants de connexion et de toutes les actions
              effectuées sous votre compte. En cas d'utilisation non autorisée de votre compte, vous devez nous en
              informer immédiatement.
            </p>
          </div>

          <!-- Section 3 -->
          <div>
            <h2 class="text-lg sm:text-xl font-bold text-[#000000] mb-2 sm:mb-3">
              3. Propriété intellectuelle
            </h2>
            <p>
              L'ensemble des éléments constituant la plateforme Vrai Besoin (textes, graphismes, logiciels,
              photographies, images, vidéos, sons, plans, noms, logos, marques, créations et œuvres protégeables
              diverses, bases de données, etc.) ainsi que le site lui-même, relèvent des législations tunisiennes et
              internationales sur le droit d'auteur et sur les droits voisins du droit d'auteur. Toute reproduction,
              représentation, diffusion ou rediffusion, totale ou partielle, du contenu de ce site par quelque procédé
              que ce soit sans l'autorisation expresse de l'éditeur est interdite.
            </p>
          </div>

          <!-- Section 4 -->
          <div>
            <h2 class="text-lg sm:text-xl font-bold text-[#000000] mb-2 sm:mb-3">
              4. Engagements et comportement de l'utilisateur
            </h2>
            <p class="mb-3">En utilisant nos services, vous vous engagez à ne pas :</p>
            <ul class="list-disc pl-5 sm:pl-6 space-y-2 mb-3 marker:text-[#9CA3AF]">
              <li>Utiliser la plateforme à des fins illégales, frauduleuses ou malveillantes.</li>
              <li>Perturber le bon fonctionnement du site, des serveurs ou des réseaux connectés.</li>
              <li>Collecter ou stocker des données personnelles d'autres utilisateurs sans leur consentement.</li>
              <li>Publier du contenu diffamatoire, obscène, offensant ou violant les droits de tiers.</li>
            </ul>
            <p>
              Nous nous réservons le droit de suspendre ou de supprimer votre accès à la plateforme en cas de
              non-respect de ces règles.
            </p>
          </div>

          <!-- Section 5 -->
          <div>
            <h2 class="text-lg sm:text-xl font-bold text-[#000000] mb-2 sm:mb-3">
              5. Limitation de responsabilité
            </h2>
            <p>
              Les informations et services proposés sur vraibesoin.me sont fournis "en l'état". Bien que nous nous
              efforcions de maintenir la plateforme accessible et à jour, nous ne pouvons garantir l'absence d'erreurs,
              de bugs ou d'interruptions de service. Notre responsabilité ne saurait être engagée en cas de dommages
              directs ou indirects résultant de l'utilisation ou de l'impossibilité d'utiliser la plateforme, y compris
              en cas de perte de données.
            </p>
          </div>

          <!-- Section 6 -->
          <div>
            <h2 class="text-lg sm:text-xl font-bold text-[#000000] mb-2 sm:mb-3">
              6. Modification des Conditions d'Utilisation
            </h2>
            <p>
              Nous nous réservons le droit de modifier, à tout moment et sans préavis, les présentes Conditions
              d'Utilisation afin de les adapter aux évolutions du site ou de la législation. La nouvelle version des CGU
              sera publiée sur cette page. Il est de votre responsabilité de consulter régulièrement ces conditions pour
              vous tenir informé des éventuelles modifications.
            </p>
          </div>

        </div>
      </section>

    </div>
  </div>
</template>

<script setup>
import SettingsPageHeader from '@/components/shared/SettingsPageHeader.vue'
</script>

<style scoped>
/*
  Ensures DM Sans is loaded for this component.
  If you already import this globally in your main.css or index.html, you can safely remove this block.
*/
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;700&display=swap');
</style>